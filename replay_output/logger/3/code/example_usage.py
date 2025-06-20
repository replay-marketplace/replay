from logger import Logger
import time

def main():
    # Create a logger with default level (INFO - 3)
    logger = Logger()
    
    print("\nRunning with default level (INFO - 3):")
    logger.critical("System is shutting down!")
    logger.error("Failed to connect to database")
    logger.warning("Low disk space")
    logger.info("User logged in")
    logger.debug("Variable x = 42")  # Won't be shown at INFO level
    
    # Change level to DEBUG to see all messages
    print("\nChanging log level to DEBUG (4):")
    logger.set_level(4)
    logger.critical("System is shutting down!")
    logger.error("Failed to connect to database")
    logger.warning("Low disk space")
    logger.info("User logged in")
    logger.debug("Variable x = 42")
    
    # Change level to WARNING to see only important messages
    print("\nChanging log level to WARNING (2):")
    logger.set_level(2)
    logger.critical("System is shutting down!")
    logger.error("Failed to connect to database")
    logger.warning("Low disk space")
    logger.info("User logged in")  # Won't be shown at WARNING level
    logger.debug("Variable x = 42")  # Won't be shown at WARNING level
    
    # Simulating a process with logs
    print("\nSimulating a process with logs:")
    logger.set_level(4)  # Set to debug to see everything
    logger.info("Starting process")
    for i in range(3):
        logger.debug(f"Processing item {i}")
        time.sleep(0.5)
        if i == 1:
            logger.warning(f"Item {i} is taking longer than expected")
    logger.error("Unexpected error occurred")
    logger.critical("Process terminated")

if __name__ == "__main__":
    main()