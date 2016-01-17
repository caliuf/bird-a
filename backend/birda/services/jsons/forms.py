#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created by caio on 08/01/16.
"""

import json
import colander
import __init__ as jsons

# ============================================================================ #
#								FORM SIMPLE
# ============================================================================ #


class FormsSimple(colander.MappingSchema):

	# Uncomment to enable the "scrict" validation
	# (i.e. raise an error if an unknown key is present)
	#
	# def schema_type(self, **kw):
	# 	return colander.Mapping(unknown='raise')

	@colander.instantiate(
		validator=colander.Length(min=1))
	class forms(colander.SequenceSchema):

		@colander.instantiate()
		class row(colander.MappingSchema):

			uri = colander.SchemaNode(
				colander.String(),
				missing=colander.required,
				validator=jsons.check_uri(required=True))

			type = colander.SchemaNode(
				colander.String(),
				missing=colander.required,
				validator=jsons.check_uri(required=True))

			label = colander.SchemaNode(
				colander.String(),
				missing=colander.required)

			description = colander.SchemaNode(
				colander.String(),
				missing=colander.required)

	# ======================================================= #

	# Coherence check
	def deserialize(self,in_json):

		res = super(FormsSimple, self).deserialize(in_json)

		# ValueError if something is not ok

		return res

# ============================================================================ #

FormSimple_example = json.loads("""
{
	"forms": [
		{
			"uri": "http://www.birda.it/form-person-1",
			"type": "http://xmlns.com/foaf/0.1/Person",
			"label": "FOAF Person Light",
			"description": "Form for editing idividuals in the FOAF Ontology.\nLight version."
		},
		{
			"uri": "http://www.birda.it/form-person-2",
			"type": "http://xmlns.com/foaf/0.1/Person",
			"label": "FOAF Person Extended",
			"description": "Form for editing idividuals in the FOAF Ontology.\nExtended version"
		},
		{
			"uri": "http://www.birda.it/fuff",
			"type": "http://xmlns.com/foaf/0.1/Fuff",
			"label": "FUFF Object",
			"description": "Nothing much here"
		}
	]
}
""", strict=False)


# ============================================================================ #
#								 FORM FULL
# ============================================================================ #

class FormsFull(colander.MappingSchema):

	# Uncomment to enable the "scrict" validation
	# (i.e. raise an error if an unknown key is present)
	#
	# def schema_type(self, **kw):
	# 	return colander.Mapping(unknown='raise')

	form_uri = colander.SchemaNode(
		colander.String(),
		missing=colander.required,
		validator=jsons.check_uri(required=True))

	maps_type = colander.SchemaNode(
		colander.String(),
		missing=colander.required,
		validator=jsons.check_uri(required=True))

	base_uri = colander.SchemaNode(
		colander.String(),
		missing=colander.required,
		validator=jsons.check_uri(required=True))

	label_property = colander.SchemaNode(
		colander.String(),
		missing=colander.required,
		validator=jsons.check_uri(required=True))

	descr_property = colander.SchemaNode(
		colander.String(),
		missing=colander.required,
		validator=jsons.check_uri(required=True))

	lang = colander.SchemaNode(
		colander.String(),
		missing=colander.required,
		validator=jsons.check_iso_lang(required=True))

	# --------------------------------- #

	@colander.instantiate(
		missing={})
	class local_name(colander.MappingSchema):

		@colander.instantiate(
			validator=colander.Length(min=1))
		class fields(colander.SequenceSchema):

			field = colander.SchemaNode(
				colander.String())

		localNameSeparator = colander.SchemaNode(
			colander.String(),
			missing=colander.drop,
			validator=colander.OneOf(['', '-', '_']))

		tokenSeparator = colander.SchemaNode(
			colander.String(),
			missing=colander.drop)

		localNameRenderer = colander.SchemaNode(
			colander.String(),
			missing=colander.drop,
			validator=colander.OneOf(['lowercase', 'uppercase', 'camelcase']))

	# ======================================================= #

	# Coherence check
	def deserialize(self,in_json):

		res = super(FormsFull, self).deserialize(in_json)

		# ValueError if something is not ok

		return res

# ============================================================================ #


FormFull_example = json.loads("""
{
	"form_uri": "http://birda.com/form-person-1",
	"maps_type": "http://xmlns.com/foaf/0.1/",
	"base_uri": "http://ex.com/",
	"label_property": "http://www.w3.org/2004/02/skos/core#prefLabel",
	"descr_property": "http://www.w3.org/2000/01/rdf-schema#comment",
	"lang": "it",
	"fields": [
		{
			"widget_uri": "http://birda.com/person-givenName-1",
			"w_type": "text-input",
			"property": "http://xmlns.com/foaf/0.1/givenName",
			"label": "Nome",
			"description": "Usare un campo diverso per ogni nome",
			"placeholder": "Nome della persona (ad es. \\\"Pino\\\")",
			"at_least": 1,
			"validation": {
				"max_length":25
			}
		},
		{
			"widget_uri": "http://birda.com/person-familyName-1",
			"w_type": "text-input",
			"property": "http://xmlns.com/foaf/0.1/familyName",
			"label": "Cognome",
			"description": "Usare un campo diverso per ogni cognome",
			"placeholder": "Cognome della persona (ad es. \\\"Rossi\\\")",
			"at_least": 1,
			"validation": {
				"max_length":25
			}
		},
		{
			"widget_uri": "http://birda.com/person-gender-1",
			"w_type": "radio-input",
			"property": "http://xmlns.com/foaf/0.1/gender",
			"label": "Genere",
			"description": "",
			"placeholder": "",
			"at_least": 1,
			"choices": [
				{
					"label": "Uomo",
					"description": "",
					"type": "xsd:string",
					"value": "http://w3id.com/gender-ontology/male"
				},
				{
					"label": "Donna",
					"description": "",
					"type": "xsd:string",
					"value": "http://w3id.com/gender-ontology/female"
				},
				{
					"label": "Non specificato",
					"description": "",
					"type": "xsd:string",
					"value": "http://w3id.com/gender-ontology/not-specified"
				}
			],
			"validation": {
				"required": true
			}
		},
		{
			"widget_uri": "http://birda.com/person-knows-1",
			"w_type": "subform",
			"maps_property": "http://xmlns.com/foaf/0.1/knows",
			"maps_type": "http://xmlns.com/foaf/0.1/",
			"label": "Persone conosciute",
			"description": "",
			"at_least": 0,
			"at_most":50,

			"fields": [
				{
					"widget_uri": "http://birda.com/person-givenName-1",
					"w_type": "text-input",
					"property": "http://xmlns.com/foaf/0.1/givenName",
					"label": "Nome",
					"description": "Usare un campo diverso per ogni nome",
					"placeholder": "Nome della persona (ad es. \\\"Pino\\\")",
					"at_least": 1,
					"validation": {
						"max_length":25
					}
				},
				{
					"widget_uri": "http://birda.com/person-familyName-1",
					"w_type": "text-input",
					"property": "http://xmlns.com/foaf/0.1/familyName",
					"label": "Cognome",
					"description": "Usare un campo diverso per ogni cognome",
					"placeholder": "Cognome della persona (ad es. \\\"Rossi\\\")",
					"at_least": 1,
					"validation": {
						"max_length":25
					}
				}
			]
		}
	],
	"local_name":{
		"fields": ["givenName", "familyMame"],
		"localNameSeparator": "_",
		"tokenSeparator": "(\\\.|\\\s|-)+",
		"localNameRenderer": "lowercase"
	}
}
""", strict=False)

# ==================================================================== #
# ==================================================================== #
# ==================================================================== #


if __name__ == '__main__':

	jsons.test_json_validation(FormsSimple, FormSimple_example, dump=True)
	jsons.test_json_validation(FormsFull, FormFull_example, dump=True)
