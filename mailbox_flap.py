from build123d import *
from ocp_vscode import *

class Flap(Compound):
    """Flap

    Mailbox Flap replacement.

    Args:
        height (float): flap height
        length (float): flap length
        barrel_diameter (float): external diameter of pin barrel
        thickness (float): flap thickness
        pin_diameter (float): flap pin diameter
        handle_width (float): handle width (depth)
        handle_height (float): handle height
        topband_height (float): barrel axis position from the top of the flap
 
        ^   
        !  / width
 height ! /   
        !/ 
        L------->
         length

    """

    def __init__(
        self,
        height: float,
        length: float,
        barrel_diameter: float,
        thickness: float,
        pin_diameter: float,
        handle_width: float,
        handle_height: float,
        topband_height: float,
    ):
        with BuildPart() as leaf_builder:
            with BuildSketch():
                with BuildLine():
                    l0 = RadiusArc(
                        (thickness, -handle_width),
                        (handle_height, 0),
                        (max(handle_height, handle_width) * 2 - thickness)
                    )
                    l1 = Line(l0 @ 1, (height, 0))
                    l2 = Line(l1 @ 1, l1 @ 1 + Vector(0, thickness))
                    l3 = Line(l2 @ 1, (handle_height, thickness))
                    l4 = RadiusArc(
                        l3 @ 1,
                        (0, -handle_width),
                        -(max(handle_height, handle_width) * 2),
                    )
                    Line(l4 @ 1, l0 @ 0)
                make_face()
                with Locations(
                    (height - topband_height - barrel_diameter / 2, barrel_diameter / 2)
                ) as pin_center:
                    Circle(barrel_diameter / 2, mode=Mode.ADD)
                    Circle(pin_diameter / 2 + 0.1 * MM, mode=Mode.SUBTRACT)
            extrude(amount=length)
        super().__init__(leaf_builder.part.wrapped, joints=leaf_builder.part.joints)

mailbox_flap = Flap(
    height=50 * MM,
    length=235 * MM,
    barrel_diameter=7 * MM,
    thickness=2 * MM,
    pin_diameter=3.75 * MM,
    handle_width=7 * MM,
    handle_height=8 * MM,
    topband_height=4 * MM,
)
# mailbox_flap.export_step("clapet_bal.step")
show(mailbox_flap)
