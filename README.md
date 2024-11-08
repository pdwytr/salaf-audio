# How to Start the App

To start the app, follow these steps:

1. **Install Dependencies**: Make sure you have all the necessary dependencies installed. You can do this by running:
    ```
    poetry install
    ```

2. **Start the Development Server**: Once the dependencies are installed, you can start the development server by running:
    ```
    poetry run start
    ```

3. **Open in Browser**: Open your web browser and navigate to `http://localhost:3000` to see the app in action.

4. **Build for Production**: If you want to build the app for production, run:
    ```
    poetry run build
    ```

Make sure you have Poetry installed on your machine before running these commands.  

5. **Run the App with Uvicorn**: To run the app using Uvicorn, execute the following command:
    ```
    poetry run uvicorn main:app --reload
    ```