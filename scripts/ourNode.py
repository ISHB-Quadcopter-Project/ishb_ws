#!/usr/bin/env python3
import rospy

def main():
    rospy.init_node("ourNode") #Make ourNode

    rospy.spin()

if __name__ =="__main__":
    main()