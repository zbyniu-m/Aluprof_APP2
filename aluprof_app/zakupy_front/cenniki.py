from flask import render_template, request, url_for, redirect, flash
from flask_wtf import FlaskForm
from aluprof_app import logger
from aluprof_app.zakupy_front import zakupy_front_bp
from aluprof_app.utils import oracle_query_to_dict
from wtforms import TextAreaField
from wtforms.validators import DataRequired
from datetime import datetime


class CennikiFormList(FlaskForm):
    list_of_items = TextAreaField('Lista bomów',
                                validators=[DataRequired("Podaj pozycję do rozbicia")],
                                render_kw={"rows": 70, "cols": 11})


@zakupy_front_bp.route('/cenniki', methods=['POST', 'GET'])
def cenniki():
    try:
        form = CennikiFormList()

        if form.validate_on_submit() and request.method == 'POST':
            lista = form.list_of_items.data.split()
            lista = "('         " + "', '         ".join(lista).upper() + "')"
            query = """select * from Book"""
            print(f'Cenniki -> IP: {request.remote_addr}, Czas: {datetime.now()}, Dane: {lista}')
            headers, pakiet = oracle_query_to_dict(query)
            return render_template('cenniki.html', form=form, dane=pakiet, headers=headers)
        else:
            return render_template('cenniki.html', form=form)
    except Exception as err:
        logger.error(
            f'{request.host_url}: Proces bomorozbijacz przerwany, Bład: {err}')
        flash(message=f'Podczas wykonywania opracji pojawił sie błąd:\n'
                      f'{err}.\n'
                      f'Skontaktuj się z administraotrem.', category='danger')
        return redirect(url_for('zakupy_front.index'))
