# Copyright (C) 2022  Tiernan8r
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
import os
import sys

# Required to guarantee that the 'qcp' module is accessible when
# this file is run directly.
if os.getcwd() not in sys.path:
    sys.path.append(os.getcwd())

import argparse
import scan


def main():
    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("image_path",
                    help="Path to the image to be scanned")
    args = vars(ap.parse_args())

    img_path = args["image_path"]

    scan.scan(img_path)


if __name__ == "__main__":
    main()
