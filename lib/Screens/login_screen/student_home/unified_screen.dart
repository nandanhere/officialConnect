import 'package:flutter_neumorphic_plus/flutter_neumorphic.dart';
import 'package:flutter_spinkit/flutter_spinkit.dart';
import 'package:official_connect/Providers/sisdata.dart';
import 'package:official_connect/Screens/login_screen/login_screen.dart';
import 'package:official_connect/Screens/login_screen/student_home/attendance_screen/attendance_screen.dart';
import 'package:official_connect/Screens/login_screen/student_home/events_screen/events_screen.dart';
import 'package:official_connect/Screens/login_screen/student_home/home_screen/home_screen.dart';
import 'package:official_connect/Screens/login_screen/student_home/results_screen/results_screen.dart';
import 'package:official_connect/Screens/login_screen/student_home/settings_screen/settings_screen.dart';
import 'package:provider/provider.dart';
import 'package:official_connect/Widgets/background_sync_status.dart';
import 'package:official_connect/Screens/login_screen/portal_refresh.dart';
import 'package:official_connect/Services/firebase_feature_flags.dart';

class Unified extends StatefulWidget {
  static const String id = 'unified';
  static final ValueNotifier<int> screenNumber = ValueNotifier(2);

  const Unified({super.key});

  @override
  State<Unified> createState() => _UnifiedState();
}

class _UnifiedState extends State<Unified> {
  late final PageController _pageController;
  final ValueNotifier<bool> _showSee = ValueNotifier(false);
  bool _automaticRefreshRequested = false;

  @override
  void initState() {
    super.initState();
    _pageController = PageController(initialPage: Unified.screenNumber.value);
  }

  @override
  void dispose() {
    _pageController.dispose();
    _showSee.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final sisData = Provider.of<SisData>(context);
    if ((sisData.usn.isEmpty && !sisData.hasData) || !sisData.isValidData) {
      return const LoginScreen();
    }
    // A stale cache is still useful and must remain navigable while a refresh
    // runs. Only block when there is genuinely nothing available to render.
    if (sisData.data.isEmpty) {
      return Scaffold(
        backgroundColor: sisData.darkMode
            ? const Color(0xff101114)
            : Colors.white,
        body: const Center(
          child: SpinKitSpinningLines(color: Color(0xffba3237), size: 80),
        ),
      );
    }

    if (!_automaticRefreshRequested &&
        sisData.hasData &&
        sisData.needToUpdate &&
        FirebaseFeatureFlags.automaticRefreshEnabled) {
      _automaticRefreshRequested = true;
      WidgetsBinding.instance.addPostFrameCallback((_) {
        if (mounted) {
          openPortalRefresh(context, allowInteractiveFallback: false);
        }
      });
    }

    final navColor = sisData.darkMode
        ? Colors.black
        : NeumorphicColors.background;
    return Scaffold(
      backgroundColor: sisData.darkMode
          ? const Color(0xff101114)
          : Colors.white,
      body: Stack(
        children: [
          PageView(
            physics: const BouncingScrollPhysics(),
            controller: _pageController,
            onPageChanged: (page) => Unified.screenNumber.value = page,
            children: [
              const EventsScreen(),
              ResultsScreen(_showSee),
              const HomeScreen(),
              const AttendanceInfo(),
              const SettingsInfo(),
            ],
          ),
          const Positioned(
            left: 16,
            right: 16,
            bottom: 12,
            child: Center(child: BackgroundSyncStatus()),
          ),
        ],
      ),
      bottomNavigationBar: ValueListenableBuilder<int>(
        valueListenable: Unified.screenNumber,
        builder: (context, selected, _) => DecoratedBox(
          decoration: BoxDecoration(
            color: navColor,
            boxShadow: [
              BoxShadow(
                color: Colors.black.withValues(alpha: 0.08),
                blurRadius: 12,
                offset: const Offset(0, -3),
              ),
            ],
          ),
          child: SafeArea(
            top: false,
            child: BottomNavigationBar(
              type: BottomNavigationBarType.fixed,
              backgroundColor: navColor,
              elevation: 0,
              currentIndex: selected,
              selectedItemColor: const Color(0xffba3237),
              unselectedItemColor: sisData.darkMode
                  ? Colors.white70
                  : Colors.black54,
              selectedFontSize: 10,
              unselectedFontSize: 10,
              selectedLabelStyle: const TextStyle(
                fontFamily: 'Comfortaa',
                fontWeight: FontWeight.bold,
              ),
              unselectedLabelStyle: const TextStyle(fontFamily: 'Comfortaa'),
              items: const [
                BottomNavigationBarItem(
                  icon: Icon(Icons.explore_outlined),
                  activeIcon: Icon(Icons.explore),
                  label: 'Explore',
                ),
                BottomNavigationBarItem(
                  icon: Icon(Icons.assessment_outlined),
                  activeIcon: Icon(Icons.assessment),
                  label: 'Results',
                ),
                BottomNavigationBarItem(
                  icon: Icon(Icons.home_outlined, size: 27),
                  activeIcon: Icon(Icons.home, size: 27),
                  label: 'Home',
                ),
                BottomNavigationBarItem(
                  icon: Icon(Icons.calendar_month_outlined),
                  activeIcon: Icon(Icons.calendar_month),
                  label: 'Attendance',
                ),
                BottomNavigationBarItem(
                  icon: Icon(Icons.settings_outlined),
                  activeIcon: Icon(Icons.settings),
                  label: 'Settings',
                ),
              ],
              onTap: (index) {
                _pageController.animateToPage(
                  index,
                  curve: Curves.easeOutCubic,
                  duration: const Duration(milliseconds: 280),
                );
              },
            ),
          ),
        ),
      ),
    );
  }
}
