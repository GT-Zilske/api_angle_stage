from src.stage_type.standa_two_axes import StandaTwoAxes

available_stages = ["StandaTwoAxes"]


class AngleStageAPI:
    def __init__(self):
        pass

    def get_stage_object(self, stage_type: str):
        if stage_type == "StandaTwoAxes":
            return StandaTwoAxes()
        else:
            raise ValueError("Invalid Angle-Stage")

    def find_connected_stages(self) -> list[str]:
        print("Not Implemented!")
