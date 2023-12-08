import undetected_chromedriver as uc

def iniciar_webdriver(headless=False,pos="max"):
    options = uc.ChromeOptions()
    options.add_argument("--pasword-store=basic")
    options.add_experimental_option(
        "prefs",
        {
            "credentials_enable_service":False,
            "profile.password_manager_enabled":False
        }
    )

    driver = uc.Chrome(
        options=options,
        log_level=3,
        headless=headless
    )

    if not headless:
        driver.maximize_window()
        if pos!="max":
            ancho,alto = driver.get_window_size().values()
            if pos == "left":
                driver.set_window_rect(x=0,y=0,width=ancho//2,height=alto)
            elif pos == "right":
                driver.set_window_rect(x=ancho//2,y=0,width=ancho//2,height=alto)
    return driver

