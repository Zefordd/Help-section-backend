from django.db.models.signals import post_save
from django.dispatch import receiver
from help.models import Section, Subsection


def _set_order(instance, created):
    if not created or instance.order != 0:
        return

    max_order = instance.get_max_order()
    instance.order = max_order + 1
    instance.save()


@receiver(post_save, sender=Section)
def set_section_order(sender, instance: Section, created, **kwargs):
    """
    Sets the order of the new section, if the order was not specified
    """
    _set_order(instance, created)


@receiver(post_save, sender=Subsection)
def set_subsection_order(sender, instance: Subsection, created, **kwargs):
    """
    Sets the order of the new subsection, if the order was not specified
    """
    _set_order(instance, created)
