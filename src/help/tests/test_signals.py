from help.models import Section, Subsection


class TestOrder:
    def test_section_order(self):
        assert Section.objects.count() == 0
        section = self._create_section('section 1')
        assert section.order == 1

        section = self._create_section('section 2')
        assert section.order == 2

        section = self._create_section('section 3', order=42)
        assert section.order == 42

    def test_subsection_order(self):
        assert Subsection.objects.count() == 0

        section_1 = self._create_section('section 1')
        subsection_1 = self._create_subsections(['subsection 1'], section_1)[0]
        assert subsection_1.order == 1
        subsection_2, subsection_3 = self._create_subsections(['subsection 2', 'subsection 3'], section_1)
        assert subsection_2.order == 2
        assert subsection_3.order == 3

        section_2 = self._create_section('section 2')
        subsection = self._create_subsections(['subsection'], section_2)[0]
        assert subsection.order == 1

    def test_updated_at_field(self):
        section = self._create_section('test_updated_at')
        old_updated_at = section.updated_at
        section.order = 2
        section.save()
        assert old_updated_at < section.updated_at

    def _create_section(self, name, order=0):
        return Section.objects.create(name=name, order=order)

    def _create_subsections(self, names, section):
        subsections = []
        for name in names:
            subsections.append(Subsection.objects.create(name=name, section=section))
        return subsections
