Example
=======

To register new document, you can compose the XML manually:

.. code-block:: python

    from cz_urnnbn_api import api

    urn_nbn = api.register_document_obj(
        api.MonographComposer(
            title="Title of the book",
            author="Name of the author",
            format="pdf"
        )
    )

or use MODS metada, if you have them:

.. code-block:: python

    from cz_urnnbn_api import 

    urn_nbn = api.register_document(
        api.convert_mono_xml(open("mods_metadata.xml").read(), "pdf")
    )

Then you can add digital instances to your ``urn_nbn`` identifiers:

.. code-block:: python

    api.register_digital_instance(
        urn_nbn=urn_nbn,
        url="someurl - lets say kramerius",
        digital_library_id="to get this, look at get_registrar_info()",
        format="epub",
        accessibility="public"
    )

For list of allowed digital libraries, call :func:`.get_registrar_info`, which
will return :class:`.Registrar` with property
:attr:`.Registrar.digital_libraries` (:class:`.DigitalLibrary`).