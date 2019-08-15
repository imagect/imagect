from zope import interface 

class ICtApp(interface.Interface) :
    """
    App Interface for imagect
    """

    def app() :
        """
        QApplication
        """
        pass 

    def mainwin() :
        """
        IMainWin
        """
        pass

    def asyncio_loop():
        """
        loop for ayncio
        """
        pass

    def rx_scheduler():
        """
        scheduler from qt ui loop
        """
        pass