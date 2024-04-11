from Point import Point
import math
class Rectangle:

    def __init__(self, center, side_length_meters):
        self.center = center
        self.side_length_meters = side_length_meters

        # Calculate the half side length in meters
        half_side_length_meters = side_length_meters / 2

        # Calculate the latitude and longitude offsets for the rectangle
        lat_offset = (180 / math.pi) * (half_side_length_meters / 6373000)
        lon_offset = (180 / math.pi) * (half_side_length_meters / 6373000) / math.cos(math.radians(center.latitude))

        # Calculate the upper left and bottom right points of the rectangle
        self.upper_left = Point(center.latitude - lat_offset, center.longitude + lon_offset)
        self.bottom_right = Point(center.latitude + lat_offset, center.longitude - lon_offset)

    # Checking if rectangle contains point
    def contains(self, latitude, longitude):
        return (self.bottom_right.latitude >= latitude >= self.upper_left.latitude and
                self.bottom_right.longitude <= longitude <= self.upper_left.longitude)
