from django.http import JsonResponse
import pandas as pd
from recommender.utils import content_based_recommend, collaborative_recommend

def recommend_view(request):
    resort_name = request.GET.get('resort', '').strip()  # Get resort name from query params

    # 🛑 Check if 'resort' parameter is missing
    if not resort_name:
        return JsonResponse({
            'error': 'Missing "resort" parameter. Example: /recommend/?resort=Crowne Plaza Kochi'
        }, status=400)

    try:
        # 🎯 Get Recommendations
        content_results = content_based_recommend(resort_name)
        collaborative_results = collaborative_recommend(resort_name)

        # 🛑 Ensure both results are DataFrames, else return empty DataFrame
        if not isinstance(content_results, pd.DataFrame):
            content_results = pd.DataFrame()  # Ensure it's an empty DataFrame
        if not isinstance(collaborative_results, pd.DataFrame):
            collaborative_results = pd.DataFrame()  # Ensure it's an empty DataFrame

        # 🛑 Handle Empty DataFrames (No recommendations)
        content_dict = content_results.to_dict(orient='records') if not content_results.empty else []
        collaborative_dict = collaborative_results.to_dict(orient='records') if not collaborative_results.empty else []

    except Exception as e:  # Catch all exceptions
        return JsonResponse({'error': str(e)}, status=500)  # Return a 500 Internal Server Error

    # ✅ Return results
    return JsonResponse({
        'content_based': content_dict,
        'collaborative': collaborative_dict
    })
