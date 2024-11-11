"""
BOOTCAMPERS TO COMPLETE.

Travel to designated waypoint and then land at a nearby landing pad.
"""

from .. import commands
from .. import drone_report

# Disable for bootcamp use
# pylint: disable-next=unused-import
from .. import drone_status
from .. import location
from ..private.decision import base_decision


# Disable for bootcamp use
# No enable
# pylint: disable=duplicate-code,unused-argument


class DecisionWaypointLandingPads(base_decision.BaseDecision):
    """
    Travel to the designed waypoint and then land at the nearest landing pad.
    """

    def __init__(self, waypoint: location.Location, acceptance_radius: float) -> None:
        """
        Initialize all persistent variables here with self.
        """
        self.waypoint = waypoint
        print(f"Waypoint: {waypoint}")

        self.acceptance_radius = acceptance_radius

        # ============
        # ↓ BOOTCAMPERS MODIFY BELOW THIS COMMENT ↓
        # ============

        self.reaching_waypoint = True
        self.reaching_landing = True
        self.at_waypoint = False
        self.landing_pad = location.Location
        self.at_landing_pad = False 
        self.has_sent_landing_command = False
        self.shortest_dis = 1000000
        #self.waypoint_to_landing_x = 0
        #self.waypoint_to_landing_y = 0

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============
    def calculate_distance(self, landing_pad: location.Location):
        # self.waypoint_to_landing_x = landing_pad.location_x - self.waypoint.location_x
        # self.waypoint_to_landing_y = landing_pad.location_y - self.waypoint.location_y
        return (landing_pad.location_x - self.waypoint.location_x)**2 + (landing_pad.location_y - self.waypoint.location_y)**2
    
    def reached_destination(self,destination: location.Location, position: location.Location):
        if (destination.location_x - position.location_x) <= self.acceptance_radius and (destination.location_y - position.location_y) <= self.acceptance_radius:
            return True
        return False

    def run(
        self, report: drone_report.DroneReport, landing_pad_locations: "list[location.Location]"
    ) -> commands.Command:
        """
        Make the drone fly to the waypoint and then land at the nearest landing pad.

        You are allowed to create as many helper methods as you want,
        as long as you do not change the __init__() and run() signatures.

        This method will be called in an infinite loop, something like this:

        ```py
        while True:
            report, landing_pad_locations = get_input()
            command = Decision.run(report, landing_pad_locations)
            put_output(command)
        ```
        """
        # Default command
        command = commands.Command.create_null_command()

        # ============
        # ↓ BOOTCAMPERS MODIFY BELOW THIS COMMENT ↓
        # ============

        # Do something based on the report and the state of this class...
        if self.reaching_waypoint:
            self.at_waypoint = self.reached_destination(self.waypoint,report.position)

            if report.status == drone_status.DroneStatus.HALTED and not self.at_waypoint:
                command = commands.Command.create_set_relative_destination_command(self.waypoint.location_x,self.waypoint.location_y)

            elif report.status == drone_status.DroneStatus.HALTED and self.at_waypoint:
                for i in range(len(landing_pad_locations)):
                    distance = self.calculate_distance(landing_pad_locations[i])
                    if distance < self.shortest_dis:
                        self.shortest_dis = distance
                        counter=i
                self.landing_pad = landing_pad_locations[counter]
                #command = commands.Command.create_set_relative_destination_command(self.waypoint_to_landing_x,self.waypoint_to_landing_y)
                command = commands.Command.create_set_relative_destination_command(self.landing_pad.location_x - self.waypoint.location_x,self.landing_pad.location_y - self.waypoint.location_y)
                self.reaching_waypoint = False
        else:
            self.at_landing_pad = self.reached_destination(self.landing_pad,report.position)

            if report.status == drone_status.DroneStatus.HALTED and not self.has_sent_landing_command and self.at_landing_pad:
                command = commands.Command.create_land_command()
                self.has_sent_landing_command = True
        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
    
    
