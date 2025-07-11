from sqlalchemy.ext.asyncio import AsyncSession

from app.models.pydantic.chat_payload import AdminPayload
from app.utils import validators
from app.services.chat_service import ChatService

application_details = {}

class ApplicationService:

    required_fields = ['name', 'email', 'company', 'job_role', 'experience']
    def __init__(self, db : AsyncSession):
        self.db = db
        self.llm = ChatService

    def hanlde_applicatoon(self, chat_data : AdminPayload):
        message = chat_data.query.strip().lower()
        session_id = chat_data.session_id

        application_details.update({
            session_id : {
                "name": None,
                "email": None,
                "company": None,
                "job_role": None,
                "experience": None
            }
        })

        if message.strip().lower() in ["cancel", "stop", "exit"]:
            application_details.pop(session_id, None)
            return "Your booking has been canceled. Let me know if you'd like to start over."
        
        if 'edit' in message:
            return self.handle_edit_request(message, session_id)
        

        
    
    def handle_edit_request(self, message: str, session_id: str):
        application = application_details.get(session_id)

        if "email" in message:
            new_email = message.split("to", 1)[-1].strip()
            if not validators.is_valid_email(new_email):
                return ("Please provide a valid email.\n\n\n"
                            "Valid email must contain a '@' and end with a domain such as '.com', '.in' etc")
            application['email'] = new_email

        elif "commpany" in message:
            new_company = message.split("to", 1)[-1].strip()
            if not validators.is_valid_company(new_company):
                return f"""Cant apply to the company {new_company}\n\n, you can only apply for the following companies:\n\n['tcs', 'cognizant', 'zoho', 'amazon', 'hcl', 'ibm', 'dxc', 'mahindra', 'tech mahindra', 'techmahindra', 'capgemini',
                           'hexaware', 'oracle', 'virtusa', 'atos', 'dell', 'mphasis', 'freshworks', 'hps', 'kissflow', 'infosys', 'wipro',
                           'lnt', 'l&t', 'ltts', 'lt', 'thoughtworks', 'altimetrik', 'photon', 'intellectdesign', 'ltimidntree', 'walmart',
                           'trimble', '3iinfotech', '3i-infotech', 'ideas2it', 'incedoinc', 'chargebee', 'xoriant', 'logitech', 'aziro', 'borngroup'
                           'hindujatech', 'inspirisys', 'birlasoft', 'spiderindia', 'way2smile', 'teamtweaks', 'pyramidionsolutions', 'happyfox',
                           'fourkites', 'contus', 'ramco', 'softsuave']"""
            application["company"] = new_company
            

        elif "job role" in message:
            new_job_role = message.split("to", 1)[-1].strip()
            application["job_role"] = new_job_role

        elif "experience" in message:
            new_experience = message.split("to", 1)[-1].strip()
            application["experience"] = new_experience

        else:
            return ("You can say things like 'Edit email to abc@xyz.com'.\n\n\n\n"
                    "Edit company to softsuave\n\n\n\n"
                    "Edit job role to Junior Python Developer\n\n\n\n"
                    "Edit experience to fresher")

        application_details[session_id] = application

        return (
            f"Updated your application:\n"
            f"- emeail: {application['email']}\n"
            f"- company: {application['company']}\n"
            f"- job role: {application['job_role']}\n"
            f"- experience: {application['experience']}\n"
            "Shall I confirm this application now? Reply with 'yes' or make further changes."
        )



        

        
