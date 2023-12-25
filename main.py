if __name__ == "__main__":
    from controller import Controller

    CONFIG_PATH = "live_config.yaml"
    controller = Controller(CONFIG_PATH)
    controller.run()
