from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from jinja2 import Template
import mjml
from app.core.mail_config import settings
import subprocess 
import subprocess
import tempfile


conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_STARTTLS=True,    # use this instead of MAIL_TLS
    MAIL_SSL_TLS=False,    # use this instead of MAIL_SSL
    USE_CREDENTIALS=True,
    TEMPLATE_FOLDER="app/email-templates"
)

import subprocess
import tempfile
import os

def compile_mjml_to_html(mjml_content: str) -> str:
    """
    Compile MJML string to HTML using MJML CLI.
    Works with MJML versions that don't support stdin (-s).
    """
    # Write MJML content to a temp file
    with tempfile.NamedTemporaryFile("w+", suffix=".mjml", delete=False) as tmp_input:
        tmp_input.write(mjml_content)
        tmp_input.flush()
        tmp_input_path = tmp_input.name

    tmp_output_path = tmp_input_path.replace(".mjml", ".html")

    try:
        # Run MJML CLI with input and output file
        subprocess.run(
            ["mjml", tmp_input_path, "-o", tmp_output_path],
            capture_output=True,
            check=True
        )

        # Read the resulting HTML
        with open(tmp_output_path, "r") as f:
            html = f.read()
        return html
    except subprocess.CalledProcessError as e:
        # MJML failed: capture error message
        error_message = e.stderr.decode("utf-8") if e.stderr else str(e)
        raise RuntimeError(f"MJML compilation failed:\n{error_message}")
    finally:
        # Clean up temp files
        os.remove(tmp_input_path)
        if os.path.exists(tmp_output_path):
            os.remove(tmp_output_path)



async def send_welcome_email(to_email: str, username: str, password: str, link: str):
    # Load MJML template
    with open("app/email-templates/welcome.mjml") as f:
        mjml_template = f.read()

    # Render with Jinja2
    mjml_rendered = Template(mjml_template).render(
        project_name="My FastAPI App",
        username=username,
        password=password,
        link=link
    )

    # Compile MJML to HTML
    html_email = compile_mjml_to_html(mjml_rendered)

    message = MessageSchema(
        subject="Welcome to My FastAPI App!",
        recipients=[to_email],
        body=html_email,
        subtype="html"
    )

    fm = FastMail(conf)
    await fm.send_message(message)
