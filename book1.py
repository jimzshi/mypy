if __name__ == '__main__':
    import MyrtaBase
    myrta = MyrtaBase.MyrtaBase()
    myrta.configure()
    myrta.read_task()
    myrta.run()