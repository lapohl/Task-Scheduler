<script src="https://cdn.jsdelivr.net/npm/chart.js@2.9.3/dist/Chart.min.js"></script>
<meta id="hrly-prec" data_hrly_prec="{{ hourly_prec }}">
    <meta id="hrly-time" data-hrly-prec="{{ time }}">
    
    <script>
      window.onload = function() {
    
        var ctx = document.getElementById('hrly-prec-Chart').getContext('2d');
        //var hrly_prec = document.getElementById('hrly-prec').data_hrly_prec();
        var hourly_prec_JSON = JSON.parse("{{hourly_prec_JSON|escapejs}}");
        var data = [];
        var dataSeries = { type: "bar" };
        var dataPoints = [];
        //var limit = hrly_prec_JSON.length;
        var time = document.getElementById("hrly-time");
    
        for (var i = 0; i < limit; i += 1) {
          dataPoints.push({
            x: i,
            //y: hrly_prec[i]
            y:20
          });
        } ;
          
        dataSeries.dataPoints = dataPoints;
        data.push(dataSeries);
      
        var options = {
          data: data  
        };
      
        var myChart = new CanvasJS.Chart(ctx, options);
        myChart.render();

        var test = document.getElementById('test');
        test.innerHTML += "{{hourly_prec_JSON|escapejs}}";

      };
    </script> 