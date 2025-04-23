# Use the official Python slim image
FROM python:3.10-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
# Set the working directory inside the container
WORKDIR /app

# Copy the project files into the container
COPY . /app
RUN uv venv
# Install dependencies
RUN pip install  -r requirements.txt

# Expose the application port
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]