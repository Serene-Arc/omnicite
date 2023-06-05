import abc
import logging
from typing import Dict, Sequence, Union

import confuse
import requests

from omnicite.exceptions import OmniCiteSourceFieldError, OmniCiteWebError, ResourceNotFound

logger = logging.getLogger(__name__)


class BaseSource(abc.ABC):
    entry_type: str = None
    required_fields: Sequence = ()
    optional_fields: Sequence = ()

    def __init__(self, identifier: str, configuration: confuse.Configuration):
        self.identifier = identifier
        self.configuration = configuration
        self.fields: Dict = dict()
        self.retrieve_information()

    @abc.abstractmethod
    def generate_unique_identifier(self, existing_identifiers: Sequence[str]) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def retrieve_information(self):
        raise NotImplementedError

    @staticmethod
    def retrieve_url(url: str, cookies: dict = None, headers: dict = None) -> requests.Response:
        try:
            res = requests.get(url, cookies=cookies, headers=headers)
        except requests.exceptions.RequestException as e:
            logger.exception(e)
            raise OmniCiteWebError(f"Failed to get page {url}")
        if res.status_code != 200:
            raise ResourceNotFound(f"Server responded with {res.status_code} to {url}")
        return res

    @staticmethod
    def check_field_existence_and_exclusivity(
        required_fields: Sequence[str | Sequence[str]],
        key_fields: Sequence[str],
    ) -> None:
        """Checks that, for each list of mutually-exclusive but required fields, that one and only one of the fields
        is present in the list of fields passed in"""
        for r in required_fields:
            if isinstance(r, str):
                if r not in key_fields:
                    raise OmniCiteSourceFieldError(f"No field found for option {r}")
                else:
                    continue
            field_existence_truth_table = [f in key_fields for f in r]
            if not any(field_existence_truth_table):
                raise OmniCiteSourceFieldError(f"No field found for any of the following options: {r}")
            elif sum(field_existence_truth_table) > 1:
                doubled_fields = [f for j, f in enumerate(r) if field_existence_truth_table[j]]
                raise OmniCiteSourceFieldError(f"Multiple exclusive fields are specified: {doubled_fields}")

    @staticmethod
    def get_all_filled_required_fields(
        required_fields: Sequence[str | Sequence[str]],
        key_fields: Sequence[str],
    ) -> Sequence[str]:
        BaseSource.check_field_existence_and_exclusivity(required_fields, key_fields)
        out = []
        for field in required_fields:
            if isinstance(field, str):
                out.append(field)
            else:
                for mutually_exclusive_option in field:
                    if mutually_exclusive_option in key_fields:
                        out.append(mutually_exclusive_option)
                        break
        return out

    @staticmethod
    def get_all_filled_optional_fields(
        optional_fields: Sequence[str | Sequence[str]],
        key_fields: Sequence[str],
    ) -> Sequence[str]:
        out = []
        for field in optional_fields:
            if isinstance(field, str):
                if field in key_fields:
                    out.append(field)
                else:
                    continue
            for subfield in field:
                if subfield in key_fields:
                    out.append(subfield)
        return out
