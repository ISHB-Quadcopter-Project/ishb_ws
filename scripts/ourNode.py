#!/usr/bin/env python3
import rospy
from nav_msgs.msg import Odometry
from geometry_msgs.msg import PoseStamped, Point
import threading
import math

GOAL_TOL = 1.0 #Tolerance for checking whether odom reading match waypoint4


class ourNode:
    def __init__(self):
        self.waypts = [
            {'x': 15.0, 'y': -3.0, 'z': 2.0},
            {'x': 0.0, 'y': -6.0, 'z': 2.0},
            {'x': 15.0, 'y': -9.0, 'z': 2.0},
            {'x': 0.0, 'y': -12.0, 'z': 2.0},
            {'x': 15.0, 'y': -15.0, 'z': 2.0},
            {'x': 0.0, 'y': -15.0, 'z': 2.0}
        ]

        self.waypt_index = 0

        self.lock = threading.Lock()
        self.latest_pos = None

        #Intializing publisher
        self.pub = rospy.Publisher("/super/goal", PoseStamped, queue_size = 10)

        #Intializing subscriber
        self.sub = rospy.Subscriber("/Odometry", Odometry, self.odom_cb, queue_size = 10)

        #Flag to see if there is available odom data to check dist_to_goal
        self.is_odom = False
    
    def publ(self):
        #Creating message to publish
        self.msg = PoseStamped() #message is an instance of class PosStamped
        self.msg.header.stamp = rospy.Time.now() #time stamp for msg
        self.msg.header.frame_id = "world" #frame of message

        print(self.waypt_index)
        self.msg.pose.position.x = self.waypts[self.waypt_index]["x"]
        self.msg.pose.position.y = self.waypts[self.waypt_index]["y"]
        self.msg.pose.position.z = self.waypts[self.waypt_index]["z"]
        self.msg.pose.orientation.w = 1.0

        self.pub.publish(self.msg)

    def odom_cb(self, msg):
        with self.lock:
            self.latest_pos = msg.pose.pose.position
            # print("INSIDE HERE IS P: ", self.latest_pos)
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

            dist_x = Odomx - self.waypts[self.waypt_index]["x"]
            dist_y = Odomy - self.waypts[self.waypt_index]["y"]
            dist_z = Odomz - self.waypts[self.waypt_index]["z"]

            squared_sum = pow(dist_x, 2) + pow(dist_y, 2) + pow(dist_z, 2)

            distance = math.sqrt(squared_sum)
            print("D: ", distance)
            if distance < GOAL_TOL:
                print("waypt reached")
                rospy.sleep(1)

                if self.waypt_index < len(self.waypts)-1:
                    self.waypt_index += 1


    def run(self):
        while(not rospy.is_shutdown()): #TODO add smt when do FSM
            # rospy.sleep(0.1)
            self.publ()
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