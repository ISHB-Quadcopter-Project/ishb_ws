#!/usr/bin/env python3
import rospy
from nav_msgs.msg import Odometry
from geometry_msgs.msg import PoseStamped, Point
import threading
import math

GOAL_TOL = 1.0 #Tolerance for checking whether odom reading match waypoint4


class ourNode:
    def __init__(self): 
        # list of dicts of waypoints
        self.waypts = [
            {'x': 15.0, 'y': -3.0, 'z': 2.0},
            {'x': 0.0, 'y': -6.0, 'z': 2.0},
            {'x': 15.0, 'y': -9.0, 'z': 2.0},
            {'x': 0.0, 'y': -12.0, 'z': 2.0},
            {'x': 15.0, 'y': -15.0, 'z': 2.0},
            {'x': 0.0, 'y': -15.0, 'z': 2.0}
        ]

        # index of waypoint list
        self.waypt_index = 0 

        self.lock = threading.Lock()

        #Odom var to hold the x,y,z odom data
        self.latest_pos = None

        #List to hold odom data, cleared every
        self.odom_list = []

        #Intializing publisher
        self.pub = rospy.Publisher("/super/goal", PoseStamped, queue_size = 10)

        #Intializing subscriber
        self.sub = rospy.Subscriber("/Odometry", Odometry, self.odom_cb, queue_size = 10)

        #Flag to see if there is available odom data to check dist_to_goal
        self.is_odom = False

        #First goal publish
        self.first_publ = True
    
    def publ(self):
        # print("Publishing now")
        #Creating message to publish
        self.msg = PoseStamped() #message is an instance of class PosStamped
        self.msg.header.stamp = rospy.Time.now() #time stamp for msg
        self.msg.header.frame_id = "world" #frame of message

        # print(self.waypt_index)
        self.msg.pose.position.x = self.waypts[self.waypt_index]["x"]
        self.msg.pose.position.y = self.waypts[self.waypt_index]["y"]
        self.msg.pose.position.z = self.waypts[self.waypt_index]["z"]
        self.msg.pose.orientation.w = 1.0

        self.pub.publish(self.msg)

    def odom_cb(self, msg):
        with self.lock:
            self.latest_pos = msg.pose.pose.position
            self.odom_list.append(self.latest_pos) #Add odom data to list for odom_watchdog
            #print("INSIDE HERE IS P: ", self.latest_pos)
            self.is_odom = True # latest_pos odom should be set by now

    def dist_to_goal(self, odom):
        # print("DIST ODOM: ", odom, "\n")

        Odomx = odom.x
        Odomy = odom.y
        Odomz = odom.z

        dist_x = Odomx - self.waypts[self.waypt_index]["x"]
        dist_y = Odomy - self.waypts[self.waypt_index]["y"]
        dist_z = Odomz - self.waypts[self.waypt_index]["z"]

        squared_sum = pow(dist_x, 2) + pow(dist_y, 2) + pow(dist_z, 2)

        distance = math.sqrt(squared_sum)
        # print("D: ", distance)
        if distance < GOAL_TOL:
            # print("waypt reached")

            if self.waypt_index < len(self.waypts)-1:
                self.waypt_index += 1
            
            self.publ() #Once reached waypoint, publish next one, instead of spamming in run

            self.is_odom = False #Set back to false, so can do this func until have odom data
    
    def odom_watchdog(self):
        #Wating until 5 secs of odom data, to see if drone moving
        if len(self.odom_list) > 50:
            delta_x = self.odom_list[-1].x - self.odom_list[0].x
            delta_y = self.odom_list[-1].y - self.odom_list[0].y

            if abs(delta_x) < 0.5 and abs(delta_y) < 0.5: #Checking if odom x and y changed, if so then publish goal again so drone move
                print("Delta x: ", delta_x)
                print("Delta y: ", delta_y)
                print("-----------I AM HAVING---------")
                self.publ()

            self.odom_list.clear()

    def run(self):
        while(not rospy.is_shutdown()): #TODO add smt when do FSM

            self.odom_watchdog() #watchdog here to run to republish if not moving, and checks length of list

            with self.lock:
                if self.is_odom == True:
                    # print("NOW HERE")
                    odom = self.latest_pos
                    self.dist_to_goal(odom) # only runs when odom is set


def main():
    rospy.init_node("ourNode") #Make ourNode

    ourNode().run()

    rospy.spin()

if __name__ =="__main__":
    main()
