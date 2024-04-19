from django.http import HttpResponseRedirect

class SaveAndSimulateMixin:
    def form_valid(self, form):

        # save the form but dont commit the changes to the database
        self.object = form.save(commit=False)

        # instead of calling the normal save, save and simulate
        self.object.save_and_simulate()

        # i dont intend on any m2m fields but keeping in case we do
        #form.save_m2m()  # Make sure to save many-to-many fields if applicable

        # do the normal return
        return HttpResponseRedirect(self.get_success_url())