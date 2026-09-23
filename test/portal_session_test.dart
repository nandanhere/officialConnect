import 'package:flutter_test/flutter_test.dart';
import 'package:official_connect/Services/portal_session.dart';

void main() {
  test('portal navigation waits for route-specific content', () {
    Uri route(String task) => Uri.parse(
      'https://parents.msrit.edu/newparents/index.php'
      '?option=com_studentdashboard&controller=studentdashboard&task=$task',
    );

    expect(
      portalExpectedContentSelector(route('timetable')),
      'table.cn-time-table, table.cn-time_table',
    );
    expect(
      portalExpectedContentSelector(route('attendencelist')),
      contains('.cn-attend-list1'),
    );
    expect(
      portalExpectedContentSelector(route('ciedetails')),
      contains('.cn-cie-stat'),
    );
    expect(
      portalExpectedContentSelector(route('observation')),
      contains('table.cn-res-table'),
    );
  });

  test('history and fee pages retain their dedicated selectors', () {
    expect(
      portalExpectedContentSelector(
        Uri.parse(
          'https://parents.msrit.edu/newparents/index.php'
          '?option=com_history&task=getResult',
        ),
      ),
      'table.res-table',
    );
    expect(
      portalExpectedContentSelector(
        Uri.parse(
          'https://parents.msrit.edu/newparents/index.php'
          '?option=com_fee&task=studFee',
        ),
      ),
      'table.cn-pay-table',
    );
  });

  test('portal failures expose only bounded diagnostic reasons', () {
    final signedUri = Uri.parse(
      'https://parents.msrit.edu/newparents/index.php?ksign=secret-token',
    );

    expect(
      portalFailureReason(PortalContentNotReadyException(signedUri)),
      'content_not_ready',
    );
    expect(
      portalFailureReason(
        PortalRequestException(signedUri, 'request timed out'),
      ),
      'timeout',
    );
    expect(
      PortalRequestException(signedUri, 'request failed').toString(),
      isNot(contains('secret-token')),
    );
  });
}
