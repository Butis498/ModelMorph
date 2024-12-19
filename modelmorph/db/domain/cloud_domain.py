from abc import ABC, abstractmethod

class CloudDomain(ABC):
    """
    An abstract base class to represent a cloud domain.

    Attributes:
    ----------
    cloud_id : str
        Unique identifier for the cloud domain.
    cloud_name : str
        Name of the cloud domain.
    cloud_type : str
        Type of the cloud domain.
    """

    def __init__(self, cloud_id: str, cloud_name: str, cloud_type: str):
        """
        Initializes the CloudDomain class with a cloud ID, name, and type.

        Parameters:
        ----------
        cloud_id : str
            Unique identifier for the cloud domain.
        cloud_name : str
            Name of the cloud domain.
        cloud_type : str
            Type of the cloud domain.
        """
        self.cloud_id = cloud_id
        self.cloud_name = cloud_name
        self.cloud_type = cloud_type

    def __str__(self):
        """
        Returns a string representation of the CloudDomain instance.

        Returns:
        -------
        str:
            String representation of the CloudDomain instance.
        """
        return f"CloudDomain(cloud_id={self.cloud_id}, cloud_name={self.cloud_name}, cloud_type={self.cloud_type})"

    def __repr__(self):
        """
        Returns a string representation of the CloudDomain instance for debugging.

        Returns:
        -------
        str:
            String representation of the CloudDomain instance.
        """
        return self.__str__()