import sys

sys.path.append("/Users/danielmathison/twigs/widgets")

from plane_calc import environment as env
from plane_calc.PlaneCalc import Plane

instance = Plane()

if __name__ == "__main__":
    instance.app.run_server(debug=True)
