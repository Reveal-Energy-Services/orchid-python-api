#
# This file is part of Orchid and related technologies.
#
# Copyright (c) 2017-2022 Reveal Energy Services.  All Rights Reserved.
#
# LEGAL NOTICE:
# Orchid contains trade secrets and otherwise confidential information
# owned by Reveal Energy Services. Access to and use of this information is 
# strictly limited and controlled by the Company. This file may not be copied,
# distributed, or otherwise disclosed outside of the Company's facilities 
# except under appropriate precautions to maintain the confidentiality hereof, 
# and may not be used in any way not expressly authorized by the Company.
#


class SearchableDataFramesWarning(Warning):
    """
    Raised when an error occurs searching for a `dpo.DomProjectObject`.
    """
    pass


class SearchableDataFramesSystemGuidWarning(SearchableDataFramesWarning):
    """
    Raised when multiple matches occur when searching for a `dpo.DomProjectObject`.
    """
    pass
