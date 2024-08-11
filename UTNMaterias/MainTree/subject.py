from abc import ABC, abstractmethod


class Subject(ABC):
    """
    This class represents a Node of the Subjects tree.
    Note: At UTN FRC (Universidad Tecnologica Nacional, Facultad Regional Cordoba),
    there's plenty states that a student can obtain by studying any subject, but we
    only need 2 of them to build this app -> Regular and Approved

    Regular: The student has passed all of his exams but he still need's to pass the final exam.
    Approved: The student has passed all of his exams, including the final exam.

    Each subject established when a student is capable of registering, it can be either
    by being "regular" or "approved" on any other previous subject

    Attributes:
        self.sql_id: int -> Represents the sql database id
        self.name: str -> The subject's name
        self.is_regular: bool -> True if the user is regular at the subject
        self.is_enrollable: bool -> True if the user can register for the subject
        self.children: list -> Represents the Subject's children.
        self.year: int -> Represents in wich year of the career is the subject
    """

    def __init__(self, sql_id: int, name: str, is_enrollable: bool) -> None:
        super().__init__()
        self.sql_id = sql_id
        self.name = name
        self.is_enrollable = is_enrollable
        self.fathers = []
        self.children = []
        self.year = None

    @abstractmethod
    def __str__(self) -> str:
        pass

    @abstractmethod
    def addChild(self, child) -> None:
        pass

    @abstractmethod
    def as_dict(self) -> dict:
        pass


class ApprovalSubject(Subject):
    """
    Represents a subject that needs to be fully approved so that the user
    can register as a student of the subject's children.

    Args:
        self.is_approved: bool -> True if the user completely finished the subject
    """

    def __init__(self, is_approved: bool, sql_id: int, name: str, is_enrollable: bool, year: int, all_approved: bool) -> None:
        super().__init__(sql_id=sql_id, name=name, is_enrollable=is_enrollable)
        self.is_approved = is_approved
        self.year = year
        self.all_approved = all_approved

    def __str__(self) -> str:
        return str(self.as_dict())

    def addChild(self, subject: Subject) -> None:
        """
        Adds a new Subject child to the current Subject

        Args:
            subject (Subject): Subject object
        """

        if isinstance(subject, ApprovalSubject):
            for child in self.children:
                if subject.sql_id == child.sql_id:
                    return
            for father in subject.fathers:
                if self.sql_id == father.sql_id:
                    return

            subject.fathers.append(self)
            self.children.append(subject)
        else:
            raise ValueError('Child must be ApprovalSubject')

    def as_dict(self) -> dict:
        list_str_children = [({'name': child.name, 'id': child.sql_id})
                             for child in self.children]
        list_str_fathers = [({'name': father.name, 'id': father.sql_id})
                            for father in self.fathers]
        data = {
            'name': self.name,
            'id': self.sql_id,
            'fathers': list_str_fathers,
            'children': list_str_children,
            'approved': self.is_approved,
            'enrollable': self.is_enrollable
        }

        return data


class RegularSubject(Subject):
    """
    Represents a subject that needs to be regular so that the user
    can register as a student of the subject's children.

    Args:
        self.regular: bool -> True if the user is regular at the subject
    """

    def __init__(self, is_regular: bool, sql_id: int, name: str, is_enrollable: bool, year: int) -> None:
        super().__init__(sql_id=sql_id, name=name, is_enrollable=is_enrollable)
        self.is_regular = is_regular
        self.year = year

    def __str__(self) -> str:
        return str(self.as_dict())

    def addChild(self, subject: Subject) -> None:
        """
        Adds a new Subject child to the current Subject

        Args:
            subject (Subject): Subject object
        """

        if isinstance(subject, RegularSubject):
            for child in self.children:
                if subject.sql_id == child.sql_id:
                    return
            for father in subject.fathers:
                if self.sql_id == father.sql_id:
                    return

            subject.fathers.append(self)
            self.children.append(subject)
        else:
            raise ValueError('Child must be RegularSubject')

    def as_dict(self) -> dict:
        list_str_children = [({'name': child.name, 'id': child.sql_id})
                             for child in self.children]
        list_str_fathers = [({'name': father.name, 'id': father.sql_id})
                            for father in self.fathers]
        data = {
            'name': self.name,
            'id': self.sql_id,
            'fathers': list_str_fathers,
            'children': list_str_children,
            'regular': self.is_regular,
            'enrollable': self.is_enrollable
        }

        return data
