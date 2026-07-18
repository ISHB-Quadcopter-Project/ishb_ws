#!/usr/bin/env python3
import rospy
from nav_msgs.msg import Odometry
from geometry_msgs.msg import PoseStamped, Point
import threading
import math

GOAL_TOL = 0.5 #Tolerance for checking whether odom reading match waypoint4


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
        self.msg.pose.position.x = 3.67
        self.msg.pose.position.y = 3.67
        self.msg.pose.position.z = 2
        self.msg.pose.orientation.w = 1.0

        self.sub = rospy.Subscriber("/Odometry", Odometry, self.odom_cb, queue_size = 10)

        self.is_odom = False

    def odom_cb(self, msg):
        with self.lock:
            self.latest_pos = msg.pose.pose.position
            # print("INSIDE HERE IS P: ", self.latest_pos)
            self.pub.publish(self.msg) #TODO change this out, and update the header w/ it too
            self.is_odom = True

    def dist_to_goal(self, odom):
        # while self.sub.get_num_connections() == 0 and not rospy.is_shutdown():
        #     print("---WAITING---")
        #     print("DIST ODOM: ", odom)
        #     rospy.sleep(0.1) #If no connection, sleep
        print("DIST ODOM: ", odom, "\n")
        if self.is_odom == True:
            Odomx = odom.x
            Odomy = odom.y
            Odomz = odom.z

            dist_x = Odomx - 3.67
            dist_y = Odomy - 3.67
            dist_z = Odomz - 2

            squared_sum = pow(dist_x, 2) + pow(dist_y, 2) + pow(dist_z, 2)

            distance = math.sqrt(squared_sum)
            print("D: ", distance)

            if distance < GOAL_TOL:
                print("waypt reached")




    def run(self):
        while(not rospy.is_shutdown()): #TODO add smt when do FSM
            rospy.sleep(0.1)
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