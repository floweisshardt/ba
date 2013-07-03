import navigation_test_helper.msg
import rospy, time

class NavigationStatusPublisher( object ):
    def __init__( self, topic, setting ):
        self._waypointNo   = -1
        self._nextWaypoint = None
        self._localtime    = time.time()
        self._publisher    = rospy.Publisher( topic, navigation_test_helper.msg.Status )
        self._setting      = setting

    def nextWaypoint( self, waypoint):
        self._waypointNo += 1
        self._nextWaypoint = waypoint
        msg = self._createMsg()
        self._publisher.publish( msg )

    def resigned( self ):
        msg = self._createMsg( 'resigned' )
        self._publisher.publish( msg )

    def timedout( self ):
        msg = self._createMsg( 'timeout' )
        self._publisher.publish( msg )

    def finished( self ):
        msg = self._createMsg( 'finished' )
        self._publisher.publish( msg )

    def _createMsg( self, info='' ):
        waypoint          = self._nextWaypoint
        msg               = navigation_test_helper.msg.Status()
        msg.header.stamp  = rospy.Time.now()
        msg.info          = info
        msg.localtime     = self._localtime
        msg.waypointId    = self._waypointNo
        msg.setting       = self._createSettingMsg()
        if waypoint:
            msg.waypointX = waypoint[ 0 ]
            msg.waypointY = waypoint[ 1 ]
            msg.waypointTheta = waypoint[ 2 ]
        return msg

    def _createSettingMsg( self ):
        msg = navigation_test_helper.msg.Setting()
        msg.robot      = self._setting[ 'robot' ]
        msg.scenario   = self._setting[ 'scenario' ]
        msg.navigation = self._setting[ 'navigation' ]
        msg.repository = self._setting[ 'repository' ]
        return msg
