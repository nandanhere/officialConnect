import re
from lxml import etree
import datetime, math,json,base64
import urllib.parse
import asyncio
import aiohttp
# from codeguru_profiler_agent import with_lambda_profiler

baseurl = "https://parents.msrit.edu/newparents/"
async def scrape_login_dashboard(respobj, body=None):
	if body is None:
		body = await respobj.content.read()
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
		find = re.findall(r'\[.*\]',attendanceOverView)
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


async def scrape_student_dashboard(session,respobj, body=None):
    # scrape all the cie / attendance links here, then call the scrape_attendance and scrape marks links here  
	d  = {}
	if body is None:
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

	




def encode_portal_password(dob):
	import base64, random, string
	noise = string.ascii_letters + string.digits
	encoded = ''.join(ch + ''.join(random.choice(noise) for _ in range(2)) for ch in dob)
	return base64.b64encode(encoded.encode()).decode()


async def login(usn, dob, captcha_response=None, otp=None):
	yy = dob[0:4]
	mm = dob[5:7]
	dd = dob[8:10]
	ret = {}
	async with aiohttp.ClientSession(trust_env=True) as session:
		async with session.get(baseurl) as resp:
			body = await resp.content.read()
			dom = etree.HTML(body)
			csrf = dom.xpath('//input[@value="1"]/@name')
			if not csrf:
				return {"validation": "portal_changed", "message": "Portal CSRF token not found"}
			if not captcha_response:
				return {"validation": "captcha_required", "message": "A reCAPTCHA token is required"}
			token = csrf[0]
			data = {
				'username': usn,
				'dd': dd,
				'mm': mm,
				'yyyy': yy,
				'passwd': encode_portal_password(dob),
				'remember': 'No',
				'option': 'com_user',
				'task': 'loginOtp',
				'return': '�w^Ƙi',
				'return': '',
				token : '1',
				'captcha-response': captcha_response,
			}
			if otp:
				data['otp'] = otp
			async with session.post(resp.url,data =data, allow_redirects=True) as resp2:
			# resp2 contains the body of text to be processed, session has to be passed among the functions.
				result_body = await resp2.read()
				result_dom = etree.HTML(result_body)
				if 'loginOtp' in str(resp2.url) or result_dom.xpath("//*[contains(translate(text(),'OTP','otp'),'otp')]"):
					return {"validation": "otp_required", "message": "The portal requires the OTP sent to the registered contact", "usn": usn}
				resp2._body = result_body
				x1 = await scrape_login_dashboard(resp2, result_body)
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


def _signed_url(url, ksign):
	"""Preserve the browser-issued signed session parameter on portal reads."""
	if not ksign:
		return url
	parts = urllib.parse.urlsplit(url)
	query = dict(urllib.parse.parse_qsl(parts.query, keep_blank_values=True))
	query.setdefault('ksign', ksign)
	return urllib.parse.urlunsplit((parts.scheme, parts.netloc, parts.path,
		urllib.parse.urlencode(query), parts.fragment))


async def scrape_authenticated_session(cookies, ksign=None, entry_url=None, user_agent=None, usn=None):
	"""Scrape using a short-lived session established by the app WebView.

	Cookies are used only for this invocation and are never logged or persisted.
	"""
	if not isinstance(cookies, list) or not cookies:
		return {'validation': 'session_required', 'message': 'Portal session cookies are required'}
	valid_cookies = []
	for cookie in cookies:
		if not isinstance(cookie, dict):
			continue
		name, value = cookie.get('name'), cookie.get('value')
		if name and value and '\n' not in name and '\r' not in name and '\n' not in value and '\r' not in value:
			valid_cookies.append((name, value))
	if not valid_cookies:
		return {'validation': 'session_required', 'message': 'No valid portal cookies were supplied'}

	headers = {
		'Cookie': '; '.join('%s=%s' % item for item in valid_cookies),
		'User-Agent': user_agent or 'OfficialConnect/1.0',
		'Accept': 'text/html,application/xhtml+xml',
	}
	timeout = aiohttp.ClientTimeout(total=25, connect=8)
	ret = {}
	async with aiohttp.ClientSession(headers=headers, timeout=timeout, trust_env=True) as session:
		landing = entry_url if isinstance(entry_url, str) and entry_url.startswith(baseurl) else baseurl + 'index.php'
		landing = _signed_url(landing, ksign)
		async with session.get(landing, allow_redirects=True) as resp:
			body = await resp.read()
			lower = body.lower()
			if b'name="username"' in lower or b'login to your account' in lower:
				return {'validation': 'session_expired', 'message': 'Portal session expired; sign in again'}
			try:
				ret.update(await scrape_login_dashboard(resp, body))
			except Exception:
				# Some accounts land directly on the student dashboard; remaining
				# endpoints still contain the complete native-app data set.
				pass

		dashboard_url = _signed_url(baseurl + 'index.php?option=com_studentdashboard&controller=studentdashboard&task=dashboard', ksign)
		async with session.get(dashboard_url) as resp:
			body = await resp.read()
			if b'name="username"' in body.lower():
				return {'validation': 'session_expired', 'message': 'Portal session expired; sign in again'}
			ret.update(await scrape_student_dashboard(session, resp, body))

		async with session.get(_signed_url(baseurl + 'index.php?option=com_history&task=getResult', ksign)) as resp:
			ret['prevResults'] = await scrape_prev_exams(resp)
		async with session.get(_signed_url(baseurl + 'index.php?option=com_studentdashboard&controller=studentdashboard&task=observation', ksign)) as resp:
			ret['proctorship'] = await scrape_proctor(resp)

	ret['usn'] = usn or ret.get('USN:') or ''
	ret['ver'] = '1.0'
	ret['downloadLink'] = ''
	return ret



async def main(usn,dob):
	x = await login(usn,dob)
	return x

def lambda_handler(event, context):
	request_body = event.get('body')
	if request_body:
		try:
			if event.get('isBase64Encoded'):
				request_body = base64.b64decode(request_body).decode('utf-8')
			payload = json.loads(request_body)
		except Exception:
			return {'statusCode': 400, 'body': json.dumps({'message': 'Invalid JSON body'})}
		if payload.get('mode') == 'session':
			result = asyncio.run(scrape_authenticated_session(
				payload.get('cookies'), payload.get('ksign'), payload.get('entryUrl'),
				payload.get('userAgent'), payload.get('usn')))
			status = 401 if result.get('validation') in ('session_required', 'session_expired') else 200
			return {
				'statusCode': status,
				'headers': {'Content-Type': 'application/json', 'Cache-Control': 'no-store'},
				'body': json.dumps(result),
			}
	params = event.get('queryStringParameters') or {}
	dob = params.get('dob')
	usn  = params.get('usn')
	if not usn or not dob:
		return {"statusCode": 400, "body": json.dumps({"message": "usn and dob are required"})}
	captcha_response = params.get('captcha_response') or params.get('captcha-response')
	otp = params.get('otp')
	if not captcha_response:
		return {"statusCode": 428, "body": json.dumps({"validation": "captcha_required", "message": "A reCAPTCHA token is required"})}
	x = asyncio.run(login(usn, dob, captcha_response, otp))
	if x.get('validation'):
		return {"statusCode": 428, "body": json.dumps(x)}

	return {
	"statusCode":200,
	"body":json.dumps(x)

	}


def sasa(usn,dob):
	x = asyncio.run(main(usn,dob))

	return {
	"statusCode":200,
	"body":json.dumps(x)

	}
# with open("./hello.json","w") as f:
# 	import json
# 	f.write(json.dumps(data,indent=3))
