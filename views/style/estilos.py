def estilo_tabela_download():
    return """
                <style> 
                    table {
                        font-family: Arial, Helvetica, sans-serif;
                        border-collapse: collapse;
                        width: 100%;
                    }

                    td, th {
                        border: 1px solid #ddd;
                        padding: 8px;
                        text-align: center;
                        vertical-align: middle;
                        
                    }

                    tr:nth-child(even){background-color: #f2f2f2;}

                    tr:hover {background-color: #ddd;}

                    th {
                        padding-top: 12px;
                        padding-bottom: 12px;
                        background-color: #04AA6D;
                        color: white;
                    }
                </style>
            """     