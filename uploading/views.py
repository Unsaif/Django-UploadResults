from django.shortcuts import render
from django.http import HttpResponse
from .forms import UploadFileForm
from .relative_abundance import gettingCols, overall, relative_abundance
import pandas as pd
import zipfile
pd.options.mode.chained_assignment = None

# Create your views here.

def upload_file(request):
    if request.method == 'POST' and request.FILES['myfile']:
        try:
            myfile = request.FILES['myfile']

            zipFileName = str(myfile).replace('.csv', '')

            data = pd.read_csv(myfile, header = 0)

            df = data[["Sample Name", "Tax Name", "Rank", "Reads"]]
            df["Sample Name"] = df["Sample Name"].replace({'.fastq.gz':''}, regex=True)
            df["Tax Name"] = df["Tax Name"].replace({'\[':'', '\]':''}, regex=True)

            dfs = df[df["Rank"] == "species"]
            dfg = df[df["Rank"] == "genus"]

            dataframeS = relative_abundance(dfs, 'Species')
            dataframeG = relative_abundance(dfg, 'Genus')

            response = HttpResponse(content_type='application/zip')

            with zipfile.ZipFile(response, 'w') as csv_zip:
                csv_zip.writestr("speciesRelativeAbundance.csv", dataframeS.to_csv(path_or_buf=None, header=True, index=True))
                csv_zip.writestr("generaRelativeAbundance.csv", dataframeG.to_csv(path_or_buf=None, header=True, index=True))

            response['Content-Disposition'] = 'attachment; filename=' + zipFileName + '.zip'

            return response
        except:
           return render(request, 'base.html', {'message': 'Incorrect file upload.'})
    return render(request, 'base.html', {'message': ''})
