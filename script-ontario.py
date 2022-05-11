from polling import OntarioPolling

polling = OntarioPolling().get_data('Ontario', data_type="share").publish("VxY9x", update_text=True)
polling = OntarioPolling(language="french").get_data('Ontario', data_type="share").publish("KTDzc")