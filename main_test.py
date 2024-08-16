from src.api_angle_stage import AngleStageAPI


def main():
    api = AngleStageAPI()
    stage = api.get_stage_object("StandaTwoAxes")
    result = stage.open_connection()
    print("connection: ", result)

    result = stage.move_relative(1, -0.1)
    result = stage.get_position(1)
    print("pos: ", result)

    result = stage.close_connection()
    print("disconnection: ", result)


if __name__ == '__main__':
    main()
