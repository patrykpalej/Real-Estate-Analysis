import os
import smtplib
from dotenv import load_dotenv
from datetime import date, datetime
from abc import ABC, abstractmethod

from scraping.orchestration.reports import (ScrapingReport,
                                            SearchScrapingReport,
                                            OffersScrapingReport)


load_dotenv()


class EmailSender(ABC):
    def __init__(self, service_name, property_type):
        self.service_name = service_name
        self.property_type = property_type

        self.sender_email_address = os.getenv("SENDER_EMAIL_ADDRESS")
        self.sender_email_password = os.getenv("SENDER_EMAIL_PASSWORD")
        self.receiver_email_address = os.getenv("RECEIVER_EMAIL_ADDRESS")
        self.smtp_address = os.getenv("SMTP_ADDRESS")
        self.smtp_port = int(os.getenv("SMTP_PORT"))

    @abstractmethod
    def _generate_title(self):
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def _generate_content(report: ScrapingReport):
        raise NotImplementedError

    def _generate_message(self, report):
        return (f"Subject: {self._generate_title()}\n\n"
                f"{self._generate_content(report)}")

    def send_email(self, report):
        message = f"Subject: {self._generate_title()}\n\n" \
                  f"{self._generate_content(report)}"

        with smtplib.SMTP(self.smtp_address, self.smtp_port) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()

            smtp.login(self.sender_email_address, self.sender_email_password)

            smtp.sendmail(self.sender_email_address,
                          self.receiver_email_address,
                          message)


class SearchEmailSender(EmailSender):
    def __init__(self, service_name, property_type):
        super().__init__(service_name, property_type)

    def _generate_title(self):
        return f"Search: {self.service_name}-{self.property_type}:" \
               f" {str(date.today())}"

    @staticmethod
    def _generate_content(report: SearchScrapingReport):
        start_str = datetime.strftime(report.scraping_started,
                                      '%Y-%m-%d %H:%M')
        end_str = datetime.strftime(report.scraping_ended, '%Y-%m-%d %H:%M')

        content = ""
        content += f"Start: {start_str}\n"
        content += f"End: {end_str}\n"
        content += f"Acquired: {report.total_n_of_urls_acquired}" \
                   f" ({report.n_of_urls_acquired_from_pages})\n"

        return content


class ScrapeEmailSender(EmailSender):
    def __init__(self, service_name, property_type):
        super().__init__(service_name, property_type)

    def _generate_title(self):
        return f"Scrape: {self.service_name}-{self.property_type}:" \
               f" {str(date.today())}"

    @staticmethod
    def _generate_content(report: OffersScrapingReport):
        start_str = datetime.strftime(report.scraping_started,
                                      '%Y-%m-%d %H:%M')
        end_str = datetime.strftime(report.scraping_ended, '%Y-%m-%d %H:%M')

        content = ""
        content += f"Start: {start_str}\n"
        content += f"End: {end_str}\n"
        content += f"Scraped before: {report.n_of_offers_scraped_before}\n"
        content += f"Unknown errors: {report.n_of_unknown_errors}\n"
        content += (f"Offers attempted: {report.total_n_of_offers_attempted}"
                    f" ({report.n_of_offers_in_packages_attempted})\n")
        content += (f"Offers success: {report.total_n_of_offers_success}"
                    f" ({report.n_of_offers_in_packages_success})\n")
        content += f"Postgresql success: {report.n_postgresql_success}\n"
        content += f"Mongodb success: {report.n_mongo_success}\n"

        return content
