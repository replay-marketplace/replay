from simple_logger import Logger

def main():
    # Create a logger that shows all messages (level 0-4)
    logger = Logger(min_level=4)
    
    # Log messages at different levels
    logger.critical("A critical error has occurred!")
    logger.error("An error has occurred, but it's not critical.")
    logger.warning("This is a warning.")
    logger.info("Just some information.")
    logger.debug("Debug information for developers.")
    
    # Create a logger that only shows important messages (level 0-2)
    important_logger = Logger(min_level=2)
    print("\nImportant messages only:")
    important_logger.critical("A critical error has occurred!")
    important_logger.error("An error has occurred, but it's not critical.")
    important_logger.warning("This is a warning.")
    important_logger.info("This info message won't be displayed.")
    important_logger.debug("This debug message won't be displayed.")
    
    # Create a logger without colors
    plain_logger = Logger(min_level=4, use_colors=False)
    print("\nLogger without colors:")
    plain_logger.critical("A critical message without colors.")
    plain_logger.info("An info message without colors.")

if __name__ == "__main__":
    main()
