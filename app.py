from flask import Flask, render_template, request
import math

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            # Retrieve form data
            RC = float(request.form['RC']) # [cite: 2]
            FY = float(request.form['FY']) # [cite: 2]
            NNP = request.form['NNP'] # [cite: 3]
            UBIC = request.form['UBIC'] # [cite: 3]
            FECHA = request.form['FECHA'] # [cite: 3]
            L = float(request.form['L']) # [cite: 3]
            CE = float(request.form['CE']) # [cite: 3]
            CD = float(request.form['CD']) # [cite: 3]
            N = float(request.form['N']) # [cite: 3]
            Q1 = float(request.form['Q1']) # [cite: 3]
            Q2 = float(request.form['Q2']) # [cite: 4]
            NS = int(request.form['NS']) # [cite: 4]
            K = int(request.form['K']) # [cite: 4]
            J = 0

            if K == 2: # [cite: 5]
                J = 2
            else:
                J = int(request.form['J']) # [cite: 5]

            # Constants from the original script
            RR = 100000.0
            E = 2100000.0
            PI = math.pi ** 2
            A = 4.267 # [cite: 5]
            P = 1.815 # [cite: 5]
            W = 18.2 # [cite: 5]

            CI = 15.24 / (L + 38.11) + 1 # [cite: 5]
            if CI > 1.3: # [cite: 5]
                CI = 1.3
            C = CI * CD * CE # [cite: 5]

            X_sections = []
            D_sections = []
            for i in range(NS):
                x_val = float(request.form[f'X_{i+1}']) # [cite: 6]
                d_val = float(request.form[f'D_{i+1}']) # [cite: 6]
                X_sections.append(x_val)
                D_sections.append(d_val)
            
            E1_sections = []
            B1_sections = []
            E2_sections = []
            B2_sections = []
            E3_sections = []
            B3_sections = []
            E4_sections = []
            B4_sections = []
            E0_sections = []
            H0_sections = []
            EL_sections = []
            BL_sections = []


            for i in range(NS):
                E1_sections.append(float(request.form[f'E1_{i+1}'])) # [cite: 9]
                B1_sections.append(float(request.form[f'B1_{i+1}'])) # [cite: 9]
                E2_sections.append(float(request.form[f'E2_{i+1}'])) # [cite: 9]
                B2_sections.append(float(request.form[f'B2_{i+1}'])) # [cite: 9]
                E3_sections.append(float(request.form[f'E3_{i+1}'])) # [cite: 9]
                B3_sections.append(float(request.form[f'B3_{i+1}'])) # [cite: 9]
                E4_sections.append(float(request.form[f'E4_{i+1}'])) # [cite: 9]
                B4_sections.append(float(request.form[f'B4_{i+1}'])) # [cite: 9]
                E0_sections.append(float(request.form[f'E0_{i+1}'])) # [cite: 9]
                H0_sections.append(float(request.form[f'H0_{i+1}'])) # [cite: 10]
                if K == 1: # [cite: 10]
                    EL_sections.append(float(request.form[f'EL_{i+1}'])) # [cite: 10]
                    BL_sections.append(float(request.form[f'BL_{i+1}'])) # [cite: 10]
                else:
                    EL_sections.append(0.0) # [cite: 11]
                    BL_sections.append(0.0) # [cite: 11]

            results = []

            for i in range(NS):
                x = X_sections[i]
                d = D_sections[i]
                E1 = E1_sections[i]
                B1 = B1_sections[i]
                E2 = E2_sections[i]
                B2 = B2_sections[i]
                E3 = E3_sections[i]
                B3 = B3_sections[i]
                E4 = E4_sections[i]
                B4 = B4_sections[i]
                E0 = E0_sections[i]
                H0 = H0_sections[i]
                EL = EL_sections[i]
                BL = BL_sections[i]

                # Calculations based on the original script
                m1 = 0.5 * Q1 * x * (L - x) # [cite: 6]
                m2 = 0.5 * Q2 * x * (L - x) # [cite: 6]

                m3 = 0.0
                if x > (L / 2 - 0.71): # [cite: 7]
                    m31 = ((L + 1.42)**2 * 9 * W / 40 / L) - 0.4 * A * W # [cite: 7]
                    m32 = (0.9 + 0.0525 * L) * W * L / 8 / 2 # [cite: 7]
                    m3 = max(m31, m32) * C # [cite: 7]
                elif x < 4.27: # [cite: 8]
                    m3 = P * x * (9 * (L - x) - 6 * A) * C / L # [cite: 8]
                else:
                    m3 = P * (9 * (L - x) - 6 * A) * x / L * C # [cite: 8]
                
                M1_i = m1 * RR # [cite: 8]
                M2_i = m2 * RR # [cite: 8]
                M3_i = m3 * RR # [cite: 8]

                AL = EL * BL # [cite: 11]
                A1 = E1 * B1 # [cite: 11]
                A2 = E2 * B2 # [cite: 11]
                A3 = E3 * B3 # [cite: 11]
                A4 = E4 * B4 # [cite: 11]
                A0 = H0 * E0 # [cite: 11]
                AV = A1 + A2 + A3 + A4 + A0 # [cite: 11]
                HV = E1 + E2 + E3 + E4 + H0 # [cite: 11]
                AP = AL / 3 / N # [cite: 12]
                AM = 3 * AP # [cite: 12]

                XT = (A4*E4/2 + A3*(E4+E3/2) + A0*(E4+E3+H0/2) + A2*(E4+E3+H0+E2/2) + A1*(E4+E3+H0+E2+E1/2)) / AV # [cite: 12]
                XC = HV - XT # [cite: 12]
                YT = (AV * XT + (HV + EL/2) * AP) / (AV + AP) if K == 1 else 0 # [cite: 12]
                YC = HV - YT # [cite: 12]
                YH = YC + EL # [cite: 13]
                ZT = (AV * XT + (HV + EL/2) * AM) / (AV + AM) if K == 1 else 0 # [cite: 13]
                ZC = HV - ZT # [cite: 13]
                ZH = ZC + EL # [cite: 13]

                IV = ((B4 * E4**3 + B3 * E3**3 + E0 * H0**3 + B2 * E2**3 + B1 * E1**3) / 12 + A4 * (XT - E4/2)**2 + A3 * (XT - E4 - E3/2)**2 + A0 * (XT - E4 - E3 - H0/2)**2 + A1 * (XC - E1/2)**2 + A2 * (XC - E1 - E2/2)**2) # [cite: 13, 14, 15]

                IVCP = IV + AP * EL**2 / 12 + AV * (YT - XT)**2 + AP * (YH - EL/2)**2 # [cite: 15]
                IVCM = IV + AM * EL**2 / 12 + AV * (ZT - XT)**2 + AM * (ZH - EL/2)**2 # [cite: 15]

                WC = IV / XC # [cite: 15]
                WT = IV / XT # [cite: 16]
                WCCP = IVCP / YC if K == 1 else 0 # [cite: 16]
                WCCM = IVCM / ZC if K == 1 else 0 # [cite: 16]
                WCTP = IVCP / YT if K == 1 else 0 # [cite: 16]
                WCTM = IVCM / ZT if K == 1 else 0 # [cite: 16]
                WCHP = IVCP / YH if K == 1 else 0 # [cite: 16]
                WCHM = IVCM / ZH if K == 1 else 0 # [cite: 16]

                fc1 = fc2 = fc3 = 0.0
                ft1 = ft2 = ft3 = 0.0
                fh1 = fh2 = fh3 = 0.0

                if K == 1: # [cite: 17]
                    if J == 1:  # Con alzaprima # [cite: 17]
                        fc3 = M3_i / WCCM # [cite: 17]
                        fc2 = (M2_i + M1_i) / WCCP # [cite: 18]
                        fc1 = 0 # [cite: 17]
                        ft3 = M3_i / WCTM # [cite: 18]
                        ft2 = (M2_i + M1_i) / WCTP # [cite: 18]
                        ft1 = 0 # [cite: 18]
                        fh3 = M3_i / (N * WCHM) # [cite: 18]
                        fh2 = (M2_i + M1_i) / (3 * N * WCHP) # [cite: 19]
                        fh1 = 0 # [cite: 19]
                    else:  # Sin alzaprima # [cite: 19]
                        fc1 = M1_i / WC # [cite: 19]
                        fc2 = M2_i / WCCP # [cite: 19]
                        fc3 = M3_i / WCCM # [cite: 19]
                        ft1 = M1_i / WT # [cite: 20]
                        ft2 = M2_i / WCTP # [cite: 20]
                        ft3 = M3_i / WCTM # [cite: 20]
                        fh1 = 0 # [cite: 20]
                        fh2 = M2_i / (3 * N * WCHP) # [cite: 20]
                        fh3 = M3_i / (N * WCHM) # [cite: 21]
                else:  # Sin losa colaborante # [cite: 21]
                    fc1 = M1_i / WC # [cite: 21]
                    fc2 = 0 # [cite: 22]
                    fc3 = M3_i / WC # [cite: 21]
                    ft1 = M1_i / WT # [cite: 21]
                    ft2 = 0 # [cite: 22]
                    ft3 = M3_i / WT # [cite: 22]
                    fh1 = fh2 = fh3 = 0 # [cite: 22]

                total_moment = (M1_i + M2_i + M3_i) / RR # [cite: 22]
                tension_comp_acero = fc1 + fc2 + fc3 # [cite: 23]
                tension_tracc_acero = ft1 + ft2 + ft3 # [cite: 23]
                tension_comp_hormigon = fh1 + fh2 + fh3 # [cite: 23]

                results.append({
                    'section_number': i + 1,
                    'x': x,
                    'd': d,
                    'total_moment': total_moment,
                    'tension_comp_acero': tension_comp_acero,
                    'tension_tracc_acero': tension_tracc_acero,
                    'tension_comp_hormigon': tension_comp_hormigon
                })
            
            return render_template('results.html', results=results, NNP=NNP, UBIC=UBIC, FECHA=FECHA, L=L, CE=CE, CD=CD, N=N, Q1=Q1, Q2=Q2, NS=NS, K=K, J=J)

        except Exception as e:
            return render_template('index.html', error=str(e))

    return render_template('index.html', NS_range=range(1, 6)) # Pass a default range for NS for initial form display

if __name__ == '__main__':
    app.run(debug=True)