# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import six

from kmip.core import enums
from kmip.core import exceptions
from kmip.core import objects
from kmip.core import primitives
from kmip.core import utils


class GetAttributesRequestPayload(primitives.Struct):
    """
    A request payload for the GetAttributes operation.

    The payload contains the ID of the managed object the attributes should
    belong to, along with a list of attribute names for the attributes that
    should be returned in the response. If the ID is omitted, the server will
    use the ID placeholder by default. If the list of attribute names is
    omitted, all object attributes will be returned. There should be no
    duplicates in the attribute name list.

    Attributes:
        uid: The unique ID of the managed object with which the retrieved
            attributes should be associated.
        attribute_names: A list of strings identifying the names of the
            attributes associated with the managed object.
    """
    def __init__(self, uid=None, attribute_names=None):
        """
        Construct a GetAttributes request payload.

        Args:
            uid (string): The ID of the managed object with which the
                retrieved attributes should be associated. Optional, defaults
                to None.
            attribute_names: A list of strings identifying the names of the
                attributes associated with the managed object. Optional,
                defaults to None.
        """
        super(GetAttributesRequestPayload, self).__init__(
            enums.Tags.REQUEST_PAYLOAD)

        self._uid = None
        self._attribute_names = list()

        self.uid = uid
        self.attribute_names = attribute_names

    @property
    def uid(self):
        if self._uid:
            return self._uid.value
        else:
            return self._uid

    @uid.setter
    def uid(self, value):
        if value is None:
            self._uid = None
        elif isinstance(value, six.string_types):
            self._uid = primitives.TextString(
                value=value,
                tag=enums.Tags.UNIQUE_IDENTIFIER
            )
        else:
            raise TypeError("uid must be a string")

    @property
    def attribute_names(self):
        if self._attribute_names:
            names = list()
            for attribute_name in self._attribute_names:
                names.append(attribute_name.value)
            return names
        else:
            return self._attribute_names

    @attribute_names.setter
    def attribute_names(self, value):
        if value is None:
            self._attribute_names = list()
        elif isinstance(value, list):
            names = list()
            for i in range(len(value)):
                name = value[i]
                if not isinstance(name, six.string_types):
                    raise TypeError(
                        "attribute_names must be a list of strings; "
                        "item {0} has type {1}".format(i + 1, type(name))
                    )
                if name not in names:
                    names.append(name)
            self._attribute_names = list()
            for name in names:
                self._attribute_names.append(
                    primitives.TextString(
                        value=name,
                        tag=enums.Tags.ATTRIBUTE_NAME
                    )
                )
        else:
            raise TypeError("attribute_names must be a list of strings")

    def read(self, istream):
        """
        Read the data encoding the GetAttributes request payload and decode
        it into its constituent parts.

        Args:
            istream (stream): A data stream containing encoded object data,
                supporting a read method; usually a BytearrayStream object.
        """
        super(GetAttributesRequestPayload, self).read(istream)
        tstream = utils.BytearrayStream(istream.read(self.length))

        if self.is_tag_next(enums.Tags.UNIQUE_IDENTIFIER, tstream):
            self._uid = primitives.TextString(tag=enums.Tags.UNIQUE_IDENTIFIER)
            self._uid.read(tstream)
        else:
            self._uid = None

        names = list()
        while self.is_tag_next(enums.Tags.ATTRIBUTE_NAME, tstream):
            name = primitives.TextString(tag=enums.Tags.ATTRIBUTE_NAME)
            name.read(tstream)
            names.append(name)
        self._attribute_names = names

        self.is_oversized(tstream)

    def write(self, ostream):
        """
        Write the data encoding the GetAttributes request payload to a
        stream.

        Args:
            ostream (stream): A data stream in which to encode object data,
                supporting a write method; usually a BytearrayStream object.
        """
        tstream = utils.BytearrayStream()

        if self._uid:
            self._uid.write(tstream)

        for attribute_name in self._attribute_names:
            attribute_name.write(tstream)

        self.length = tstream.length()
        super(GetAttributesRequestPayload, self).write(ostream)
        ostream.write(tstream.buffer)

    def __repr__(self):
        uid = "uid={0}".format(self.uid)
        attribute_names = "attribute_names={0}".format(self.attribute_names)
        return "GetAttributesRequestPayload({0}, {1})".format(
            uid,
            attribute_names
        )

    def __str__(self):
        return str({
            'uid': self.uid,
            'attribute_names': self.attribute_names
        })

    def __eq__(self, other):
        if isinstance(other, GetAttributesRequestPayload):
            if self.uid == other.uid:
                if set(self.attribute_names) == set(other.attribute_names):
                    return True
                else:
                    return False
            else:
                return False
        else:
            return NotImplemented

    def __ne__(self, other):
        if isinstance(other, GetAttributesRequestPayload):
            return not self.__eq__(other)
        else:
            return NotImplemented


class GetAttributesResponsePayload(primitives.Struct):
    """
    A response payload for the GetAttributes operation.

    The payload will contain the ID of the managed object with which the
    attributes are associated. It will also contain a list of attributes
    associated with the aforementioned managed object.

    Attributes:
        uid: The unique ID of the managed object with which the retrieved
            attributes should be associated.
        attributes: The list of attributes associated with managed object
            identified by the uid above.
    """
    def __init__(self, uid=None, attributes=None):
        """
        Construct a GetAttributes response payload.

        Args:
            uid (string): The ID of the managed object with which the
                retrieved attributes should be associated. Optional, defaults
                to None.
            attributes (list): A list of attribute structures associated with
                the managed object. Optional, defaults to None.
        """
        super(GetAttributesResponsePayload, self).__init__(
            enums.Tags.RESPONSE_PAYLOAD)

        self._uid = None
        self._attributes = list()

        self.uid = uid
        self.attributes = attributes

    @property
    def uid(self):
        if self._uid:
            return self._uid.value
        else:
            return self._uid

    @uid.setter
    def uid(self, value):
        if value is None:
            self._uid = None
        elif isinstance(value, six.string_types):
            self._uid = primitives.TextString(
                value=value,
                tag=enums.Tags.UNIQUE_IDENTIFIER
            )
        else:
            raise TypeError("uid must be a string")

    @property
    def attributes(self):
        return self._attributes

    @attributes.setter
    def attributes(self, value):
        if value is None:
            self._attributes = list()
        elif isinstance(value, list):
            for i in range(len(value)):
                attribute = value[i]
                if not isinstance(attribute, objects.Attribute):
                    raise TypeError(
                        "attributes must be a list of attribute objects; "
                        "item {0} has type {1}".format(i + 1, type(attribute))
                    )
            self._attributes = value
        else:
            raise TypeError("attributes must be a list of attribute objects")

    def read(self, istream):
        """
        Read the data encoding the GetAttributes response payload and decode
        it into its constituent parts.

        Args:
            istream (stream): A data stream containing encoded object data,
                supporting a read method; usually a BytearrayStream object.
        """
        super(GetAttributesResponsePayload, self).read(istream)
        tstream = utils.BytearrayStream(istream.read(self.length))

        if self.is_tag_next(enums.Tags.UNIQUE_IDENTIFIER, tstream):
            uid = primitives.TextString(tag=enums.Tags.UNIQUE_IDENTIFIER)
            uid.read(tstream)
            self.uid = uid.value
        else:
            raise exceptions.InvalidKmipEncoding(
                "expected GetAttributes response uid not found"
            )

        self._attributes = list()
        while self.is_tag_next(enums.Tags.ATTRIBUTE, tstream):
            attribute = objects.Attribute()
            attribute.read(tstream)
            self._attributes.append(attribute)

        self.is_oversized(tstream)

    def write(self, ostream):
        """
        Write the data encoding the GetAttributes response payload to a
        stream.

        Args:
            ostream (stream): A data stream in which to encode object data,
                supporting a write method; usually a BytearrayStream object.
        """
        tstream = utils.BytearrayStream()

        if self._uid:
            self._uid.write(tstream)
        else:
            raise exceptions.InvalidField(
                "The GetAttributes response uid is required."
            )

        for attribute in self._attributes:
            attribute.write(tstream)

        self.length = tstream.length()
        super(GetAttributesResponsePayload, self).write(ostream)
        ostream.write(tstream.buffer)

    def __repr__(self):
        uid = "uid={0}".format(self.uid)
        names = "attributes={0}".format(self.attributes)
        return "GetAttributesResponsePayload({0}, {1})".format(uid, names)

    def __str__(self):
        return str({'uid': self.uid, 'attributes': self.attributes})

    def __eq__(self, other):
        if isinstance(other, GetAttributesResponsePayload):
            if self.uid != other.uid:
                return False
            if len(self._attributes) != len(other._attributes):
                return False
            for i in range(len(self._attributes)):
                a = self._attributes[i]
                b = other._attributes[i]
                if a != b:
                    return False
            return True
        else:
            return NotImplemented

    def __ne__(self, other):
        if isinstance(other, GetAttributesResponsePayload):
            return not self.__eq__(other)
        else:
            return NotImplemented
