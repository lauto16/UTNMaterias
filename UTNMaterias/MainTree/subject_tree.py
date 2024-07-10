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
        self.children: list = Represents the Subject's children.
    """

    def __init__(self, sql_id: int, name: str, is_enrollable: bool) -> None:
        super().__init__()
        self.sql_id = sql_id
        self.name = name
        self.is_enrollable = is_enrollable
        self.children = []

    @abstractmethod
    def __str__(self) -> str:
        pass

    @abstractmethod
    def addChild(self, child) -> None:
        pass


class ApprovalSubject(Subject):
    """
    Represents a subject that needs to be fully approved so that the user 
    can register as a student of the subject's children.

    Args:
        self.is_approved: bool -> True if the user completely finished the subject
    """

    def __init__(self, is_approved: bool, sql_id: int, name: str, is_enrollable: bool) -> None:
        super().__init__(sql_id=sql_id, name=name, is_enrollable=is_enrollable)
        self.is_approved = is_approved

    def __str__(self) -> str:
        str_children = [child.name for child in self.children]
        r = str(
            f'ID: {self.sql_id}\n' +
            f'NAME: {self.name}\n' +
            f'CHILDREN: {str_children}\n' +
            f'IS_APPROVED: {self.is_approved}\n' +
            f'IS_ENROLLABLE: {self.is_enrollable}\n'
        )
        return r

    def addChild(self, subject) -> None:
        """
        Adds a new Subject child to the current Subject

        Args:
            subject (Subject): Subject object
        """

        if isinstance(subject, ApprovalSubject):
            # verificar que no exista ya en el arbol
            #
            self.children.append(subject)
        else:
            raise ValueError('Child must be ApprovalSubject')


class SubjectTree(ABC):
    """
    A Tree that containt Subject objects as nodes.

    Attributes:
    self.root: Represents the root Subject (father of all the Subjects),
    in this case is normally 'Ingreso'.
    """

    def __init__(self, root: Subject) -> None:
        super().__init__()
        self.root = root

    @abstractmethod
    def search(self, sql_id: int, actual_subject: Subject):
        """
        Given a certain sql_id and actual_subject, it looks for the actual_subject children whose sql_id
        matches with the one passed as an argument 

        Args:
            sql_id (int): Subject's sql id
            actual_subject: Subject's father
        Returns:
            None: if the subject doesn't exist
            Subject. if the subject was found
        """
        pass

    @abstractmethod
    def addSubject(self, father_sql_id: int, child_subject: Subject) -> None:
        """
        Adds a new child subject to a given father subject

        Args:
            father_sql_id (int): Father's sql id
            child_subject (Subject): Child to add            
        """
        pass


class ApprovalTree(SubjectTree):
    """
    A Tree that contains ApprovalSubject objects as nodes, representing
    the approval path that any student follows to finish the career
    """

    def __init__(self) -> None:
        ingreso = ApprovalSubject(is_approved=False,
                                  sql_id=1, name='Ingreso', is_enrollable=True)
        super().__init__(root=ingreso)

    def search(self, sql_id: int, actual_subject: ApprovalSubject):
        if actual_subject.sql_id == sql_id:
            return actual_subject
        for child in actual_subject.children:
            found = self.search(sql_id=sql_id, actual_subject=child)
            if found:
                return found
        return None

    def addSubject(self, father_sql_id: int, child_subject: ApprovalSubject) -> None:
        father_subject = self.search(
            sql_id=father_sql_id, actual_subject=self.root)
        if father_subject:
            father_subject.addChild(child_subject)
        else:
            raise Exception("Couldn't add the subject, father doesn't exist")


# TEST AREA------------------------------------------------------------------------------------------------------------------------
ami = ApprovalSubject(is_approved=False, sql_id=2,
                      name='Analisis matematico 1', is_enrollable=True)

an = ApprovalSubject(is_approved=False, sql_id=3,
                     name='Analisis numerico', is_enrollable=False)

eco = ApprovalSubject(is_approved=False, sql_id=4,
                      name='Economia', is_enrollable=False)


fis1 = ApprovalSubject(is_approved=False, sql_id=5,
                       name='Fisica 1', is_enrollable=False)

fis3 = ApprovalSubject(is_approved=False, sql_id=6,
                       name='Fisica 3', is_enrollable=False)

com = ApprovalSubject(is_approved=False, sql_id=7,
                      name='Comunicacion de datos', is_enrollable=False)


t = ApprovalTree()

t.addSubject(father_sql_id=1, child_subject=ami)
t.addSubject(father_sql_id=1, child_subject=fis1)

t.addSubject(father_sql_id=2, child_subject=an)
t.addSubject(father_sql_id=2, child_subject=eco)

t.addSubject(father_sql_id=5, child_subject=fis3)
t.addSubject(father_sql_id=5, child_subject=com)


print(t.search(0, t.root))
