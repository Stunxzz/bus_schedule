
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import mixins

from bus_schedule.bus.forms import ScheduleForm
import pandas as pd

from bus_schedule.bus.models import ScheduleModel



class ScheduleCreateView(mixins.LoginRequiredMixin, generic.CreateView):
    form_class = ScheduleForm
    template_name = "upload.html"
    success_url = reverse_lazy('schedule')

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.save()

        return super().form_valid(form)



def schedule_show_view(request):
    try:
        schedule_model = ScheduleModel.objects.last()
        print(schedule_model)
        if schedule_model:
            header = ""
            excel_path = schedule_model.excel.path
            dp = pd.read_excel(excel_path)
            #dp = dp.loc[:, ~dp.columns.str.contains('Unnamed')]
            dp.dropna(axis=0, how="all", inplace=True)
            dp.dropna(axis=1, how='all', inplace=True)
            header = True

            dp = dp.fillna("")
            dp.columns = dp.columns.astype(str)
            for index, row in dp.iterrows():
                print(f"row:-------{row}--------")

            for colum in dp.columns:
                if all("Unnamed:" in column for column in dp.columns):
                    header = False
                    first_row = dp.iloc[0]
                    for i in range(len(first_row)):
                        cell_value = dp.iloc[0, i]
                        if "00:00:00" in str(cell_value):
                            date_hours = str(cell_value).split()
                            new_value = date_hours[0]
                            dp.iloc[0, i] = new_value

                if "00:00:00" in colum:
                    list_colum = colum.split()
                    dp.columns = dp.columns.str.replace(list_colum[1], "")

                elif "Unnamed:" in colum:
                    dp.columns = dp.columns.str.replace(str(colum), "")
            for c in dp.columns:
                if c != "" and len(c) < 11:
                    dp.drop(str(c),axis=1, inplace=True)

            table_html = dp.to_html(index=False)

        else:
            table_html = "Няма налични данни за графика."
    except Exception as e:

        table_html = f"Грешка при зареждане на данните: {str(e)}"


    return render(request, 'schedule.html', {'table_html': table_html})


