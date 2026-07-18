#!/usr/bin/env python3
import rospy
from nav_msgs.msg import Odometry
from geometry_msgs.msg import PoseStamped

def main():
    rospy.init_node("ourNode") #Make ourNode

    #Intializing publisher
    pub = rospy.Publisher("/super/goal", PoseStamped, queue_size = 10)

    #Wait until get a connection
    while pub.get_num_connections() == 0 and not rospy.is_shutdown():
        rospy.sleep(0.1) #If no connection, sleep

    #Creating bare bone message to publish
    msg = PoseStamped() #message is an instance of class PosStamped
    msg.header.stamp = rospy.Time.now() #time stamp for msg
    msg.header.frame_id = "world" #frame of message
    msg.pose.position.x = 6.67
    msg.pose.position.y = 6.67
    msg.pose.position.z = 6.67
    msg.pose.orientation.w = 1.0
    pub.publish(msg)



    rospy.spin()

if __name__ =="__main__":
    main()