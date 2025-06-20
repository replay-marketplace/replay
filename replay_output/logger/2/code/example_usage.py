from logger import Logger

def main():
    # Create a logger with default settings (level 4, output to stdout)
    logger = Logger()
    
    # Log messages at different levels
    logger.critical("System failure! Database connection lost.")
    logger.error("Unable to process request due to missing parameters.")
    logger.warning("Resource usage above 80%.")
    logger.info("User 'admin' logged in successfully.")
    logger.debug("Processing request with parameters: {id=123, action='update'}")
    
    print("\n--- Setting log level to 2 (WARNING) ---")
    # Change the log level to only show messages with level <= 2
    logger.set_level(2)
    
    # Now only CRITICAL, ERROR, and WARNING messages will be displayed
    logger.critical("This critical message will be shown.")
    logger.error("This error message will be shown.")
    logger.warning("This warning message will be shown.")
    logger.info("This info message will NOT be shown.")
    logger.debug("This debug message will NOT be shown.")

if __name__ == "__main__":
    main()
