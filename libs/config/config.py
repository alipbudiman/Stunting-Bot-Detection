class Config:
    """Configuration class for web application settings.

    This class manages configuration settings for a web application, including:
    - Application secret key for security
    - WhatsApp OTP server address for authentication
    - MongoDB connection URI

    Attributes:
        APP_SECRET (str): Secret key used for web application security
        SERVER_WA_OTP_ADDRESS (str): URL endpoint for WhatsApp OTP service
        MONGDB_URI (str): MongoDB connection string for database access

    Note:
        WhatsApp OTP bot is required for sending PIN verification to users.
        Contact developer at 082113791904 for OTP bot integration,
        or build custom solution using example at:
        https://github.com/alipbudiman/Go-OpenAI-WhatsApp-Bot
    """
    def __init__(self) -> None:
        # web app secret key (add by yourself)
        self.APP_SECRET = "(@B2d~9.%$yoR8Yj0S.vyAS#.;sycuy}yBFPs-mpXL=aDS=-;f"
        # you need otp bot to send otp to send pin to user WA
        # if you need otp bot, you can contact me (082113791904)
        # or you can build by yourself, example using wa bot here:
        # https://github.com/alipbudiman/Go-OpenAI-WhatsApp-Bot
        self.SERVER_WA_OTP_ADDRESS = "http:otp_host:8010"
        # add your mongdb uri here
        self.MONGDB_URI = "mongodb://username:password@host1:port1,host2:port2/database?"