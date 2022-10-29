import re
from lxml import etree
import datetime, math,json
import asyncio
import aiohttp
# from codeguru_profiler_agent import with_lambda_profiler

baseurl = "http://parents.msrit.edu/"
# baseurl = "https://parents.msrit.edu/parents_even2022/"
async def scrape_login_dashboard(respobj):
	body = await respobj.content.read()
	print(body.text)
    # scrape all the fee data here. 
	# print(respobj.text)
	# soup = BeautifulSoup(respobj.content,'lxml', from_encoding="utf8")
	dom = etree.HTML(body)
	firstScreenData = {}
	studdetailshead = dom.xpath('//*[@class="cn-basic-details"]/table/tbody/tr/td/span/text()')
	studdetailstable = dom.xpath('//*[@class="cn-basic-details"]/table/tbody/tr/td/text()')
	
	studimage = dom.xpath('//img[@class="uk-preserve-width uk-border"]/@src')[-1]
	firstScreenData['studentImage'] = baseurl + '/' + studimage

	for x,y in zip(studdetailshead,studdetailstable):
		firstScreenData[x.strip()] = y.strip()
	# # note that there is a table for fees paid and one for refunds. 
	tables =  dom.xpath('//*[@class="uk-table uk-table-striped uk-table-hover cn-pay-table uk-table-middle"]')
	refunds = []
	fees = []

	# # NOTE : For refund details, they did not use th. they used td. so if there is a small change that might be the soln 
	for table in tables:
		capt = table.xpath('./caption/text()')[0]
		if capt == "Payment Updated":
			head = [i.strip() for i in table.xpath('.//thead/tr/th//text()')]
			for row in table.xpath('./tbody/tr'):
				d = {}
				for h,data in zip(head,row.xpath('./td//text()')):
					d[h] = data.strip()
				fees.append(d)
				# print(d)

		elif capt == "Refund Details":
			head = [i.strip() for i in table.xpath('.//thead/tr/td//text()')]	
			for row in table.xpath('./tbody/tr'):
				d = {}
				for h,data in zip(head,row.xpath('./td//text()')):
					d[h] = data.strip()
				refunds.append(d)

	firstScreenData['refunds'] = refunds
	firstScreenData['fees'] = fees
	return firstScreenData




async def scrape_prev_exams(respobj):
	# soup = BeautifulSoup(respobj.content,'lxml', from_encoding="utf8")
	body = await respobj.content.read()
	dom = etree.HTML(body)
	x = dom.xpath('//*[contains(@class,"uk-table uk-table-striped res-table")]')
	results = []
	for table in x:
		d = {}
		data = [t.strip().split(':') for t in table.xpath('./caption/span/text()')]
		for item in data:
			d[item[0]] = item[-1]
		caption = table.xpath('./caption/text()')[0]
		d['term'] = caption.strip()
		subjects = []
		headers = [header.strip() for header in table.xpath('./thead/tr/th/text()')]
		headers[0] = "".join(headers[0].split(" ")).replace('\n',' ')
		for row in table.xpath('./tbody/tr'):
			ret = []
			dd = {}
			for data in row.xpath('./td/text()'):
				ret.append(data.strip())
			for header,item in zip(headers,ret):
				dd[header] = item
			subjects.append(dd)
		d['results'] = subjects
		results.append(d)
	# print(results)

	return results

async def scrape_proctor(respobj):
	# soup = BeautifulSoup(respobj.content,'lxml', from_encoding="utf8")
	body = await respobj.content.read()
	dom = etree.HTML(body)
	# print(soup.text)
	d = {}
	proctorname = dom.xpath('//h3[@class="md-card-head-text uk-margin-small"]/text()')
	proctordeets = dom.xpath('//h3[@class="md-card-head-text uk-margin-small"]/span/text()')
	table = dom.xpath('//table[@class="uk-table uk-table-striped cn-res-table uk-table-middle uk-table-justify uk-table-small"]//tr')
	messages = []
	def getText(text):
		ret = ""
		flip = 0
		for i in text:
			if (i != ">" and i != '<') and flip == 0:
				ret += i
			flip += 1 if i == "<" else -1 if i == ">" else 0
		return ret
				
	for row in table:
		message = {}
		try:
			data = [getText(t.itertext()) for t in row.xpath('./td')]
			if not data: continue
			message['date'],message['sender'],message['desc'] = data
		except Exception as e:
			print(e)
		messages.append(message)
	d = {'proctorial_notes': messages}
	d['proctor_name'] = "No data" if not proctorname else "".join(proctorname).strip()
	d['branch'] = "No data" if not proctordeets else proctordeets[0]
	d['email'] = "No data" if not proctordeets else proctordeets[1]
	d['phone'] = "No data" if not proctordeets else proctordeets[2]
	# print(d)
	return d


def scrape_attendance(text):
	# do this for each attendance link. there are attendance links for each subject
	att = dict()
	dom = etree.HTML(text)
	try:
		# Note that details should be in the order : [subject code - name, teacher email id , phone number]
		tmp = dom.xpath('//h3[@class="md-card-head-text"]/span/text()')
		details = tmp if len(tmp) != 0 else dom.xpath('//h3[@class="md-card-head-text uk-margin-remove"]/span/text()')
		inter = [x for x in details[0].split() if x != '-']
		att['code'] , att['name'] = inter[0]," ".join(inter[1:])
		# teacher name
		tmp = dom.xpath('//h3[@class="md-card-head-text"]/text()')
		att['teacher'] = tmp[0].strip() if len(tmp) != 0 else dom.xpath('//h3[@class="md-card-head-text uk-margin-remove"]/text()')[0].strip()
		# Getting attendance stats
		#attendanceOverView must be in the format present, absent, remaining , so just use re and get all of them in one go
		attendanceOverView = "".join(dom.xpath('//div[@class="cn-legend"]//text()'))
		# print(attendanceOverView)
		find = re.findall('\[.*\]',attendanceOverView)
		attendanceOverView = [x[1:-1] for x in find]
		attendanceOverView = [x if x != '' else "0" for x in attendanceOverView]
		att['present'],att['absent'],att['remaining'] = attendanceOverView
		total = int(att['present']) + int(att['absent'])
		att['percentage'] = str('0' if total == 0 else math.floor((int(attendanceOverView[0]) / total) * 100)) + "%"
		# log([att])
		

		# Getp{resent}a{ttendance} will give you a list of dictionaries of the dates of classes
		def getpa(extracted):
			d = dict()
			counter = 0
			ret = []
			for s in extracted:
				if counter == 1:
					d['date'] = s.strip() 
				if counter == 2:
					d['time'] = '-'.join([i.strip() for i in s.split("TO")])
					d['index'] = str(counter)
					d['status'] = 'None'
					ret.append(d)
					d = {}
				counter += 1
				counter %= 4
			return ret

		present = getpa(dom.xpath('//table[@class="uk-table uk-table-small cn-attend-list1 uk-table-striped"]/tbody/tr/td/text()'))
		absent = getpa(dom.xpath('//table[@class="uk-table uk-table-small cn-attend-list2 uk-table-striped"]/tbody/tr/td/text()'))
			# this we do so that in ui you can show latest dates for the  classes first (we can change)
		absent = sorted(absent, key=lambda x:datetime.datetime.strptime(x['date'],"%d-%m-%Y"),reverse=True)
		present = sorted(present, key=lambda x:datetime.datetime.strptime(x['date'],"%d-%m-%Y"),reverse=True)
		att['present_dates'] = present
		att['absent_dates'] = absent
		
	except Exception as e:
		print(["Error in attendance scrape : ", e])
		return {}

	return att
		


	#  Example output
	# 	  "code": "MAOE04",  done
    #     "name": "Applied Graph Theory", done
    #     "teacher": "Azghar Pasha.B", 	done
    #     "present": "32",
    #     "absent": "5",
    #     "remaining": "0",
    #     "percentage": "86%",
    #     "present_dates":[]
	
def scrape_marks(text):
	marks = dict()
	response = etree.HTML(text)

	try :
		graph = response.xpath('//div[@class="uk-card  uk-card-body cn-cie-stat"]//script/text()')[0]
		averages = {}
		marks['name'] = response.xpath('//th[@colspan="9"]/text()')[0]
		headers = ['t1','t2','t3','t4','a1','a2','a3']
		for h,v in zip(headers,  re.findall(r'"col1": (\d+)',graph)):
			averages[h] = v
		marks['class_average'] = averages
		name = list(marks['name'])
		index = name.index('(')
		name[index] = ' '
		name[index+1] = '('
		marks['name'] = ''.join(name[:len(marks['name'])-1])

		all_marks=response.xpath('//tr[@class="odd"]/td[@class=""]/text()')
		for i in range(7):
			if all_marks[i] == '%' or all_marks[i] == '':
				all_marks[i] = '-'
		for head,val in zip(headers,all_marks[:7]):
			marks[head] = val

		try:	
			marks['final cie'] = all_marks[7]
		except:
			marks['final cie'] = '-'
		
	except Exception as e:
		print(["Error in marks scrape",e])
		return {}
	return marks
		

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.content.read()


async def scrape_student_dashboard(session,respobj):
    # scrape all the cie / attendance links here, then call the scrape_attendance and scrape marks links here  
	d  = {}
	body = await respobj.content.read()
	response = etree.HTML(body)
	details = response.xpath('//a/@href')
	d = {}
	d['name'] = response.xpath('//div[@class="uk-card uk-card-body cn-stu-data cn-stu-data1"]/h3/text()')[0]
	a  = response.xpath('//div[@class="uk-card uk-card-body cn-stu-data"]/p/text()')[0].split(',')
	b  = response.xpath('//div[@class="cn-legend"]/span/text()')		
	d['courseSmall'],d['sem'],d['sec'] = [n.strip() for n in a]
	d['earned'],d['to_earn']= b[0].split()[0].strip(),b[1].split()[0].strip()
	attendanceLinks =  []
	cieLinks = []
	for deet in details:
		if 'ciedetails' in deet:
			cieLinks.append(deet)
		elif 'attendencelist' in deet:
			attendanceLinks.append(deet)
	marks = []
	attendance = []
	mtasks = []
	atasks = []

	# create tasks for each of the attendances and marks := problem in lambda is that requests are slow. so we do all of them in paralell so that we get responses
	# quicker. here we do attendances first then marks. processing the requests takes little to no time.
	for i in attendanceLinks:
		atasks.append(fetch(session,baseurl + i))
	htmls1 = await asyncio.gather(*atasks)
	for i in cieLinks:
		mtasks.append(fetch(session,baseurl + i))
	htmls2 = await asyncio.gather(*mtasks)
	attendance = [scrape_attendance(i) for i in htmls1]
	marks = [scrape_marks(i) for i in htmls2]
	d["attendance"] = attendance
	d["marks"] = marks
	return d

	




async def login(usn,dob):
	yy = dob[0:4]
	mm = dob[5:7]
	dd = dob[8:10]
	ret = {}
	async with aiohttp.ClientSession(trust_env=True) as session:
		async with session.get(baseurl) as resp:
			body = await resp.content.read()
			dom = etree.HTML(body)
			token = dom.xpath('//input[@value="1"]/@name')[0]
			data = {
				'username': usn,
				'dd': dd,
				'mm': mm,
				'yyyy': yy,
				'passwd': dob,
				'remember': 'No',
				'option': 'com_user',
				'task': 'login',
				'return': '�w^Ƙi',
				'return': '',
				token : '1'
			}
			async with session.post(resp.url,data =data) as resp2:
		# resp2 contains the body of text to be processed, session has to be passed among the functions.
				x1 = await scrape_login_dashboard(resp2)
				ret.update(x1)
			async with session.get(baseurl + "index.php?option=com_studentdashboard&controller=studentdashboard&task=dashboard") as resp3:
				x = await scrape_student_dashboard(session,resp3)
				ret.update(x)
			async with session.get(baseurl + "index.php?option=com_history&task=getResult") as resp4:
				ret["prevResults"] = await scrape_prev_exams(resp4)
			async with session.get(baseurl + "index.php?option=com_studentdashboard&controller=studentdashboard&task=observation") as resp5:
				ret["proctorship"] = await scrape_proctor(resp5)

			

			ret["usn"] = usn

			
			ret["downloadLink"]=  "https://www.dl.dropboxusercontent.com/s/1keww8izjzs727a/officialConnectv03.apk?dl=0"
			ret[ "ver"] = "0.3"
	return ret



async def main(usn,dob):
	x = await login(usn,dob)
	return x

def lambda_handler(event, context):
	dob = event['queryStringParameters']['dob']
	usn  = event['queryStringParameters']['usn']
	loop = asyncio.get_event_loop()
	x = loop.run_until_complete(main(usn,dob))

	return {
	"statusCode":200,
	"body":json.dumps(x)

	}


def sasa(usn,dob):
	loop = asyncio.get_event_loop()
	x = loop.run_until_complete(main(usn,dob))

	return {
	"statusCode":200,
	"body":json.dumps(x)

	}
import time
t = time.time()
print(sasa("1ms19is076","2000-12-08"))
print(time.time() - t)


# with open("./hello.json","w") as f:
# 	data = login("1MS19IS076","2000-12-08")	#nandan
# 	import json
# 	f.write(json.dumps(data,indent=3))