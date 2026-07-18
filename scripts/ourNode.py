#!/usr/bin/env python3
import rospy
from nav_msgs.msg import Odometry
from geometry_msgs.msg import PoseStamped
import threading

GOAL_TOL = 1 #Tolerance for checking whether odom reading match waypoint4
POS = 0

class ourNode:
    def __init__(self):
        self.lock = threading.Lock()
        self.latest_pos = None

        #Intializing publisher
        self.pub = rospy.Publisher("/super/goal", PoseStamped, queue_size = 10)

        #Creating bare bone message to publish
        self.msg = PoseStamped() #message is an instance of class PosStamped
        self.msg.header.stamp = rospy.Time.now() #time stamp for msg
        self.msg.header.frame_id = "world" #frame of message
        self.msg.pose.position.x = 6.67
        self.msg.pose.position.y = 6.67
        self.msg.pose.position.z = 6.67
        self.msg.pose.orientation.w = 1.0

        self.sub = rospy.Subscriber("/Odometry", Odometry, self.odom_cb, queue_size = 10)

    def odom_cb(self, msg):
        with self.lock:
            self.latest_pos = msg.pose.pose.position
            print("INSIDE HERE IS P: ", self.latest_pos)
            self.pub.publish(self.msg)

    def dist_to_goal(self, odom):
        print("DIST ODOM: ", odom)

    def run(self):
        #TODO some sorta if statement here to know idk reached or right pos
        while(1):
            with self.lock:
                odom = self.latest_pos
                self.dist_to_goal(odom)
        
    






def main():
    rospy.init_node("ourNode") #Make ourNode

    ourNode().run()

    #Intializing publisher
    # pub = rospy.Publisher("/super/goal", PoseStamped, queue_size = 10)

    # #Wait until get a connection
    # while pub.get_num_connections() == 0 and not rospy.is_shutdown():
    #     rospy.sleep(0.1) #If no connection, sleep

    # #Creating bare bone message to publish
    # msg = PoseStamped() #message is an instance of class PosStamped
    # msg.header.stamp = rospy.Time.now() #time stamp for msg
    # msg.header.frame_id = "world" #frame of message
    # msg.pose.position.x = 6.67
    # msg.pose.position.y = 6.67
    # msg.pose.position.z = 6.67
    # msg.pose.orientation.w = 1.0
    # pub.publish(msg)
    
    # #Initlizing subscriber
    # def odom_cb(msg):
    #     with threading.Lock():
    #         POS = msg.pose.pose.position
    #         print("INSIDE HERE IS P: ", POS)
    
    # # print("HERE IS P: ", POS)
    
    # sub = rospy.Subscriber("/Odometry", Odometry, odom_cb, queue_size = 10)
    
    #Checking if at waypoint
    # reached = False
    # while(not reached):
    #     with threading.Lock():
    #         # print("HERE IS P: ", POS)



    rospy.spin()

if __name__ =="__main__":
    main()