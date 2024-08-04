from abc import ABC, abstractmethod
from .models import UTNSubject
import json


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

    def __init__(self, is_approved: bool, sql_id: int, name: str, is_enrollable: bool, year: int) -> None:
        super().__init__(sql_id=sql_id, name=name, is_enrollable=is_enrollable)
        self.is_approved = is_approved
        self.year = year

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

    def str_constructor(self, actual_subject, tree_str='', indent_level=0) -> str:
        """
        Builds the tree diagram

        Returns:
            str: Tree diagram with identation
        """

        tree_str = '|———' * indent_level + \
            actual_subject.name + f'({actual_subject.sql_id})'
        for child in actual_subject.children:
            tree_str += '\n' + \
                self.str_constructor(
                    actual_subject=child, tree_str=tree_str, indent_level=indent_level+1)

        return tree_str

    def __str__(self) -> str:
        return self.str_constructor(actual_subject=self.root)

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


class RegularTree(SubjectTree):
    """
    A Tree that contains RegularSubjects objects as nodes, representing
    the regularity path that any student follows to finish the career
    """

    def __init__(self, root) -> None:
        super().__init__(root=root)

    def __str__(self) -> str:
        return super().__str__()

    def search(self, sql_id: int, actual_subject: RegularSubject):
        if actual_subject.sql_id == sql_id:
            return actual_subject
        for child in actual_subject.children:
            found = self.search(sql_id=sql_id, actual_subject=child)
            if found:
                return found
        return None

    def addSubject(self, father_sql_id: int, child_subject: RegularSubject) -> None:
        father_subject = self.search(
            sql_id=father_sql_id, actual_subject=self.root)
        if father_subject:
            father_subject.addChild(child_subject)
        else:
            raise Exception("Couldn't add the subject, father doesn't exist")


class ApprovalTree(SubjectTree):
    """
    A Tree that contains ApprovalSubject objects as nodes, representing
    the approval path that any student follows to finish the career
    """

    def __init__(self, root) -> None:
        super().__init__(root=root)

    def __str__(self) -> str:

        return super().__str__()

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


class SubjectTreeDB():
    """
    Creates a Tree, containing subjects as nodes, it can be either ApprovalTree or RegularTree

    Args:
        career (str): must be: sistemas, mecanica, metalurgica, electronica, electrica, industrial or quimica
        type (str): must be: 'approval' or 'regular'
    """

    def __init__(self, career: str, tree_type: str) -> None:
        self.career = career
        self.tree_type = tree_type
        self.tree = self.create(tree_type=self.tree_type, career=self.career)

    @classmethod
    def parseStrList(self, str_list: str) -> list:
        """
        Parse from str('int,int') to list(int,int)
        example: '1,2,3,4' -> [1,2,3,4]

        Args:
            str_list (str): A str with the following format -> '1,2,3,4'

        Returns:
            list: A list containing int elements separeted by commas
        """
        if str_list == '':
            return []

        final_list = []
        number = ''
        for char in str_list:

            if char == ',':
                final_list.append(int(number))
                number = ''
                continue

            elif char.isdigit():
                number += char

        final_list.append(int(number))
        return final_list

    def travel_tree(self, actual_subject: Subject, nodes=[]) -> list:
        """
        Travels the entire tree returning a list of all the nodes

        Args:
            actual_subject (Subject): The subject where the traveling starts
            nodes (list, optional): List that will contain all the nodes through the recursive stack. Defaults to [].

        Returns:
            list: A list of nodes
        """
        if actual_subject.year == 0:
            nodes.append(actual_subject)
        for child in actual_subject.children:
            nodes.append(child)
            self.travel_tree(actual_subject=child, nodes=nodes)

        return nodes

    def as_dict(self) -> dict:
        """
        Returns the SubjectTree represented as a dictionary

        {
            'year0':[
                {
                    id: 1,
                    name: 'Analisis matematico',
                    children: [2,3,5]
                    ...
                },
            ]

        }

        Returns:
            dict: Tree represented as dictionary
        """
        children = self.travel_tree(actual_subject=self.tree.root)
        children_by_year = [[] for _ in range(7)]
        added = []

        for child in children:
            if child.sql_id in added:
                continue
            children_by_year[child.year].append(child)
            added.append(child.sql_id)

        for year_list in children_by_year:
            year_list.sort(key=lambda x: x.sql_id)

        year_subject_dict = {}
        for year, year_list in enumerate(children_by_year):
            key = 'year_' + str(year)
            year_subject_dict[key] = year_list
            for i, subject in enumerate(year_list):

                if self.tree_type == 'approval':
                    subject_dict = {
                        'id': subject.sql_id,
                        'name': subject.name,
                        'children': [x.sql_id for x in subject.children],
                        'fathers': [x.sql_id for x in subject.fathers],
                        'is_approved': subject.is_approved,
                        'is_enrollable': subject.is_enrollable
                    }
                    year_list[i] = subject_dict

                elif self.tree_type == 'regular':
                    subject_dict = {
                        'id': subject.sql_id,
                        'name': subject.name,
                        'children': [x.sql_id for x in subject.children],
                        'fathers': [x.sql_id for x in subject.fathers],
                        'is_regular': subject.is_regular,
                        'is_enrollable': subject.is_enrollable
                    }
                    year_list[i] = subject_dict

        return year_subject_dict

    def create(self, tree_type: str, career: str) -> SubjectTree:
        """
        Builds the tree structure using the database data

        Args:
            career (str): must be: sistemas, mecanica, metalurgica, electronica, electrica, industrial or quimica
            type (str): must be: 'approval' or 'regular'

        Returns:
            SubjectTree: when the transaction was successfull and the tree was created correctly
        """
        tree = None

        if tree_type == 'approval':
            ingreso = UTNSubject.objects.get(approval_fathers=career)
            ingreso_subject = ApprovalSubject(
                is_approved=False, sql_id=ingreso.id, name=ingreso.name, is_enrollable=True, year=0)

            tree = ApprovalTree(root=ingreso_subject)
            ingreso_children_ids = self.parseStrList(ingreso.approval_children)

            tree = self.recursive_approval_tree_build(
                sql_ids=ingreso_children_ids, tree=tree, actual_subject=tree.root, added_nodes=[tree.root.sql_id])

        elif tree_type == 'regular':
            ingreso = UTNSubject.objects.get(regular_fathers=career)
            ingreso_subject = RegularSubject(
                is_regular=False, sql_id=ingreso.id, name=ingreso.name, is_enrollable=True, year=0)

            tree = RegularTree(root=ingreso_subject)
            ingreso_children_ids = self.parseStrList(ingreso.regular_children)

            tree = self.recursive_regular_tree_build(
                sql_ids=ingreso_children_ids, tree=tree, actual_subject=tree.root, added_nodes=[tree.root.sql_id])

        return tree

    def recursive_approval_tree_build(self, tree: SubjectTree, sql_ids: list, actual_subject: Subject, added_nodes: list) -> SubjectTree:
        """
        Generates an approval tree using recursion an database info.

        Args:
            tree (SubjectTree): Base tree
            sql_ids (list): Ingreso subject children sql_id's list
            added_nodes (list): The nodes that already exist at the tree
            actual_subject (Subject): The current subject
        """
        for sql_id in sql_ids:
            # ami, aga, etc...
            child_subject = UTNSubject.objects.get(id=sql_id)
            child = ApprovalSubject(
                is_approved=False, is_enrollable=False, name=child_subject.name, sql_id=child_subject.id, year=child_subject.year)

            if child.sql_id in added_nodes:
                found_subject = tree.search(
                    sql_id=child.sql_id, actual_subject=tree.root)
                if found_subject:
                    actual_subject.addChild(found_subject)

            else:
                actual_subject.addChild(child)
                added_nodes.append(child.sql_id)

            self.recursive_approval_tree_build(tree=tree, sql_ids=self.parseStrList(
                child_subject.approval_children), actual_subject=child, added_nodes=added_nodes)

        return tree

    def recursive_regular_tree_build(self, tree: SubjectTree, sql_ids: list, actual_subject: Subject, added_nodes: list) -> SubjectTree:
        """
        Generates a regularity tree using recursion an database info.

        Args:
            tree (SubjectTree): Base tree
            sql_ids (list): Ingreso subject children sql_id's list
            added_nodes (list): The nodes that already exist at the tree
            actual_subject (Subject): The current subject
        """
        for sql_id in sql_ids:
            # ami, aga, etc...
            child_subject = UTNSubject.objects.get(id=sql_id)
            child = RegularSubject(
                is_regular=False, is_enrollable=False, name=child_subject.name, sql_id=child_subject.id, year=child_subject.year)

            if child.sql_id in added_nodes:
                found_subject = tree.search(
                    sql_id=child.sql_id, actual_subject=tree.root)
                if found_subject:
                    actual_subject.addChild(found_subject)

            else:
                actual_subject.addChild(child)
                added_nodes.append(child.sql_id)

            self.recursive_regular_tree_build(tree=tree, sql_ids=self.parseStrList(
                child_subject.regular_children), actual_subject=child, added_nodes=added_nodes)

        return tree

# TEST AREA------------------------------------------------------------------------------------------------------------------------


if __name__ == '__main__':
    pass
