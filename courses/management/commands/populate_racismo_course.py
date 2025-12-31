"""
Django management command to add sample content to "Combate ao racismo inclusivo" course.
This creates modules, lessons, quizzes, and questions as test data.
"""

from django.core.management.base import BaseCommand
from courses.models import (
    Course, Module, Lesson, Quiz, Question, QuestionOption, QuizQuestion
)


class Command(BaseCommand):
    help = 'Add sample content to Combate ao racismo inclusivo course'

    def handle(self, *args, **kwargs):
        # Get the course
        try:
            course = Course.objects.get(name__icontains='Combate ao racismo')
        except Course.DoesNotExist:
            self.stdout.write(self.style.ERROR('Course "Combate ao racismo inclusivo" not found'))
            return

        self.stdout.write(f'Adding content to course: {course.name}')

        # Clear existing content
        course.modules.all().delete()

        # ===== MODULE 1: Introdução ao Racismo Estrutural =====
        module1 = Module.objects.create(
            course=course,
            title='Módulo 1: Introdução ao Racismo Estrutural',
            description='Compreenda os conceitos fundamentais do racismo estrutural e suas manifestações na sociedade.',
            order=1,
            is_published=True
        )

        Lesson.objects.create(
            module=module1,
            title='O que é Racismo Estrutural?',
            content='''
            <h2>Definição de Racismo Estrutural</h2>
            <p>O racismo estrutural é um conceito que descreve como o racismo está enraizado nas estruturas sociais, políticas e econômicas de uma sociedade. Não se trata apenas de atos individuais de discriminação, mas de um sistema que perpetua desigualdades raciais através de instituições, políticas e práticas.</p>
            
            <h3>Características Principais:</h3>
            <ul>
                <li><strong>Sistêmico:</strong> Está presente em todas as instituições da sociedade</li>
                <li><strong>Histórico:</strong> Tem raízes em processos históricos de colonização e escravidão</li>
                <li><strong>Normalizado:</strong> Muitas vezes é invisível para quem não é afetado</li>
                <li><strong>Reprodutivo:</strong> Se perpetua através de gerações</li>
            </ul>
            
            <h3>Exemplos na Prática:</h3>
            <p>O racismo estrutural se manifesta em diversas áreas:</p>
            <ul>
                <li>Mercado de trabalho: menor acesso a cargos de liderança</li>
                <li>Educação: desigualdade no acesso a ensino de qualidade</li>
                <li>Saúde: diferenças no atendimento e nos resultados de saúde</li>
                <li>Justiça: maior encarceramento de pessoas negras</li>
            </ul>
            ''',
            video_url='https://www.youtube.com/watch?v=example1',
            duration_minutes=15,
            order=1,
            is_published=True
        )

        Lesson.objects.create(
            module=module1,
            title='História do Racismo no Brasil',
            content='''
            <h2>Contexto Histórico</h2>
            <p>O Brasil foi o último país das Américas a abolir a escravidão, em 1888. Mais de 300 anos de escravidão deixaram marcas profundas na sociedade brasileira.</p>
            
            <h3>Linha do Tempo:</h3>
            <ul>
                <li><strong>1500-1888:</strong> Período escravocrata - mais de 4 milhões de africanos escravizados</li>
                <li><strong>1888:</strong> Lei Áurea - abolição sem políticas de integração</li>
                <li><strong>1889-1930:</strong> Políticas de branqueamento da população</li>
                <li><strong>1930-1988:</strong> Mito da democracia racial</li>
                <li><strong>1988-hoje:</strong> Reconhecimento do racismo e políticas afirmativas</li>
            </ul>
            
            <h3>Consequências Atuais:</h3>
            <p>A falta de políticas de reparação após a abolição resultou em:</p>
            <ul>
                <li>Desigualdade econômica persistente</li>
                <li>Segregação espacial nas cidades</li>
                <li>Sub-representação política</li>
                <li>Estereótipos e preconceitos arraigados</li>
            </ul>
            ''',
            video_url='',
            duration_minutes=20,
            order=2,
            is_published=True
        )

        # Quiz for Module 1
        quiz1 = Quiz.objects.create(
            module=module1,
            title='Avaliação: Racismo Estrutural',
            description='Teste seus conhecimentos sobre racismo estrutural',
            passing_score=70,
            max_attempts=3,
            time_limit_minutes=15,
            order=3,
            is_published=True
        )

        # Questions for Quiz 1
        q1 = Question.objects.create(
            course=course,
            question_text='O que caracteriza o racismo estrutural?',
            question_type='MC',
            explanation='O racismo estrutural é sistêmico, ou seja, está presente nas estruturas e instituições da sociedade, não apenas em atos individuais.',
            points=10
        )
        QuestionOption.objects.create(question=q1, option_text='Apenas atos individuais de discriminação', is_correct=False, order=1)
        QuestionOption.objects.create(question=q1, option_text='Um sistema que perpetua desigualdades através de instituições', is_correct=True, order=2)
        QuestionOption.objects.create(question=q1, option_text='Preconceito pessoal contra raças', is_correct=False, order=3)
        QuestionOption.objects.create(question=q1, option_text='Diferenças culturais entre grupos', is_correct=False, order=4)
        QuizQuestion.objects.create(quiz=quiz1, question=q1, order=1)

        q2 = Question.objects.create(
            course=course,
            question_text='Em que ano foi abolida a escravidão no Brasil?',
            question_type='MC',
            explanation='A Lei Áurea, que aboliu a escravidão no Brasil, foi assinada em 13 de maio de 1888.',
            points=10
        )
        QuestionOption.objects.create(question=q2, option_text='1822', is_correct=False, order=1)
        QuestionOption.objects.create(question=q2, option_text='1888', is_correct=True, order=2)
        QuestionOption.objects.create(question=q2, option_text='1889', is_correct=False, order=3)
        QuestionOption.objects.create(question=q2, option_text='1930', is_correct=False, order=4)
        QuizQuestion.objects.create(quiz=quiz1, question=q2, order=2)

        q3 = Question.objects.create(
            course=course,
            question_text='O racismo estrutural afeta apenas o mercado de trabalho.',
            question_type='TF',
            explanation='Falso. O racismo estrutural afeta todas as áreas da sociedade: educação, saúde, justiça, moradia, etc.',
            points=10
        )
        QuestionOption.objects.create(question=q3, option_text='Verdadeiro', is_correct=False, order=1)
        QuestionOption.objects.create(question=q3, option_text='Falso', is_correct=True, order=2)
        QuizQuestion.objects.create(quiz=quiz1, question=q3, order=3)

        # ===== MODULE 2: Práticas Inclusivas =====
        module2 = Module.objects.create(
            course=course,
            title='Módulo 2: Práticas Inclusivas no Ambiente de Trabalho',
            description='Aprenda estratégias práticas para promover inclusão racial em organizações.',
            order=2,
            is_published=True
        )

        Lesson.objects.create(
            module=module2,
            title='Recrutamento e Seleção Inclusivos',
            content='''
            <h2>Estratégias para Recrutamento Inclusivo</h2>
            <p>Um processo de recrutamento inclusivo é fundamental para aumentar a diversidade racial nas organizações.</p>
            
            <h3>Boas Práticas:</h3>
            <ul>
                <li><strong>Divulgação ampla:</strong> Anunciar vagas em canais diversos, incluindo organizações focadas em diversidade</li>
                <li><strong>Descrição inclusiva:</strong> Evitar linguagem que possa afastar candidatos diversos</li>
                <li><strong>Critérios objetivos:</strong> Definir requisitos claros e mensuráveis</li>
                <li><strong>Painéis diversos:</strong> Incluir pessoas de diferentes origens nas entrevistas</li>
                <li><strong>Treinamento anti-viés:</strong> Capacitar recrutadores sobre vieses inconscientes</li>
            </ul>
            
            <h3>Vieses Inconscientes a Evitar:</h3>
            <ul>
                <li>Viés de afinidade (contratar pessoas similares a nós)</li>
                <li>Viés de confirmação (buscar informações que confirmem impressões iniciais)</li>
                <li>Efeito halo (deixar uma característica influenciar toda avaliação)</li>
                <li>Estereótipos raciais</li>
            </ul>
            ''',
            video_url='https://www.youtube.com/watch?v=example2',
            duration_minutes=25,
            order=1,
            is_published=True
        )

        Lesson.objects.create(
            module=module2,
            title='Criando um Ambiente Acolhedor',
            content='''
            <h2>Ambiente de Trabalho Inclusivo</h2>
            <p>Criar um ambiente onde todos se sintam valorizados e respeitados é essencial para retenção de talentos diversos.</p>
            
            <h3>Elementos Fundamentais:</h3>
            <ul>
                <li><strong>Política clara:</strong> Código de conduta explícito contra discriminação</li>
                <li><strong>Liderança comprometida:</strong> Apoio visível da alta gestão</li>
                <li><strong>Grupos de afinidade:</strong> Espaços seguros para troca de experiências</li>
                <li><strong>Mentoria:</strong> Programas de desenvolvimento para profissionais negros</li>
                <li><strong>Comunicação aberta:</strong> Canais para reportar discriminação</li>
            </ul>
            
            <h3>Ações Práticas:</h3>
            <ul>
                <li>Celebrar datas importantes (Dia da Consciência Negra, etc.)</li>
                <li>Promover palestras e workshops sobre diversidade</li>
                <li>Revisar materiais de comunicação para inclusão</li>
                <li>Garantir representatividade em materiais visuais</li>
                <li>Criar oportunidades iguais de desenvolvimento</li>
            </ul>
            ''',
            video_url='',
            duration_minutes=20,
            order=2,
            is_published=True
        )

        # Quiz for Module 2
        quiz2 = Quiz.objects.create(
            module=module2,
            title='Avaliação: Práticas Inclusivas',
            description='Avalie seu entendimento sobre práticas inclusivas',
            passing_score=70,
            max_attempts=3,
            time_limit_minutes=10,
            order=3,
            is_published=True
        )

        q4 = Question.objects.create(
            course=course,
            question_text='Qual NÃO é uma boa prática de recrutamento inclusivo?',
            question_type='MC',
            explanation='Contratar apenas por indicação de funcionários atuais pode perpetuar a falta de diversidade, pois as pessoas tendem a indicar pessoas similares a elas.',
            points=10
        )
        QuestionOption.objects.create(question=q4, option_text='Divulgar vagas em canais diversos', is_correct=False, order=1)
        QuestionOption.objects.create(question=q4, option_text='Treinar recrutadores sobre vieses', is_correct=False, order=2)
        QuestionOption.objects.create(question=q4, option_text='Contratar apenas por indicação de funcionários', is_correct=True, order=3)
        QuestionOption.objects.create(question=q4, option_text='Usar critérios objetivos de seleção', is_correct=False, order=4)
        QuizQuestion.objects.create(quiz=quiz2, question=q4, order=1)

        q5 = Question.objects.create(
            course=course,
            question_text='Cite uma ação prática para criar um ambiente de trabalho mais inclusivo.',
            question_type='SA',
            explanation='Exemplos de respostas: criar grupos de afinidade, promover palestras sobre diversidade, celebrar datas importantes, garantir representatividade em materiais visuais, etc.',
            points=10
        )
        QuizQuestion.objects.create(quiz=quiz2, question=q5, order=2)

        # ===== MODULE 3: Combate ao Racismo no Dia a Dia =====
        module3 = Module.objects.create(
            course=course,
            title='Módulo 3: Combate ao Racismo no Cotidiano',
            description='Estratégias práticas para identificar e combater o racismo em situações do dia a dia.',
            order=3,
            is_published=True
        )

        Lesson.objects.create(
            module=module3,
            title='Identificando Microagressões',
            content='''
            <h2>O que são Microagressões?</h2>
            <p>Microagressões são comentários, ações ou comportamentos sutis que comunicam mensagens hostis ou negativas sobre grupos marginalizados.</p>
            
            <h3>Exemplos Comuns:</h3>
            <ul>
                <li>"Você é muito articulado para uma pessoa negra"</li>
                <li>Tocar no cabelo de pessoas negras sem permissão</li>
                <li>"De onde você é REALMENTE?"</li>
                <li>Seguir pessoas negras em lojas</li>
                <li>Assumir que uma pessoa negra é menos qualificada</li>
            </ul>
            
            <h3>Impacto das Microagressões:</h3>
            <ul>
                <li>Acumulação causa estresse crônico</li>
                <li>Afeta saúde mental e física</li>
                <li>Cria ambiente hostil</li>
                <li>Reduz produtividade e engajamento</li>
            </ul>
            
            <h3>Como Responder:</h3>
            <ul>
                <li>Reconheça o impacto, não apenas a intenção</li>
                <li>Peça esclarecimento: "O que você quis dizer com isso?"</li>
                <li>Eduque quando apropriado</li>
                <li>Estabeleça limites claros</li>
                <li>Busque apoio quando necessário</li>
            </ul>
            ''',
            video_url='https://www.youtube.com/watch?v=example3',
            duration_minutes=18,
            order=1,
            is_published=True
        )

        Lesson.objects.create(
            module=module3,
            title='Sendo um Aliado Antirracista',
            content='''
            <h2>O Papel do Aliado</h2>
            <p>Ser antirracista significa tomar ações ativas contra o racismo, não apenas não ser racista.</p>
            
            <h3>Princípios da Aliança:</h3>
            <ul>
                <li><strong>Educação contínua:</strong> Aprender sobre racismo e suas manifestações</li>
                <li><strong>Escuta ativa:</strong> Ouvir experiências de pessoas negras sem defensividade</li>
                <li><strong>Amplificação:</strong> Usar privilégios para dar voz a pessoas marginalizadas</li>
                <li><strong>Ação:</strong> Intervir quando presenciar racismo</li>
                <li><strong>Responsabilidade:</strong> Assumir erros e aprender com eles</li>
            </ul>
            
            <h3>Ações Práticas:</h3>
            <ul>
                <li>Questionar piadas e comentários racistas</li>
                <li>Apoiar negócios de pessoas negras</li>
                <li>Votar em políticas antirracistas</li>
                <li>Educar familiares e amigos</li>
                <li>Reconhecer e usar seus privilégios</li>
                <li>Participar de movimentos antirracistas</li>
            </ul>
            
            <h3>O que NÃO fazer:</h3>
            <ul>
                <li>Esperar que pessoas negras eduquem você</li>
                <li>Centralizar sua própria experiência</li>
                <li>Buscar validação por ser "um dos bons"</li>
                <li>Desistir quando cometer erros</li>
            </ul>
            ''',
            video_url='',
            duration_minutes=22,
            order=2,
            is_published=True
        )

        # Final Quiz
        quiz3 = Quiz.objects.create(
            module=module3,
            title='Avaliação Final do Curso',
            description='Teste final abrangente sobre todo o conteúdo do curso',
            passing_score=75,
            max_attempts=2,
            time_limit_minutes=20,
            order=3,
            is_published=True
        )

        q6 = Question.objects.create(
            course=course,
            question_text='O que são microagressões?',
            question_type='MC',
            explanation='Microagressões são comportamentos sutis que comunicam mensagens hostis ou negativas sobre grupos marginalizados.',
            points=10
        )
        QuestionOption.objects.create(question=q6, option_text='Agressões físicas leves', is_correct=False, order=1)
        QuestionOption.objects.create(question=q6, option_text='Comentários sutis que comunicam mensagens negativas', is_correct=True, order=2)
        QuestionOption.objects.create(question=q6, option_text='Apenas piadas ofensivas', is_correct=False, order=3)
        QuestionOption.objects.create(question=q6, option_text='Críticas construtivas', is_correct=False, order=4)
        QuizQuestion.objects.create(quiz=quiz3, question=q6, order=1)

        q7 = Question.objects.create(
            course=course,
            question_text='Ser antirracista significa apenas não ser racista.',
            question_type='TF',
            explanation='Falso. Ser antirracista significa tomar ações ativas contra o racismo, não apenas evitar comportamentos racistas.',
            points=10
        )
        QuestionOption.objects.create(question=q7, option_text='Verdadeiro', is_correct=False, order=1)
        QuestionOption.objects.create(question=q7, option_text='Falso', is_correct=True, order=2)
        QuizQuestion.objects.create(quiz=quiz3, question=q7, order=2)

        q8 = Question.objects.create(
            course=course,
            question_text='Descreva duas ações práticas que você pode tomar para ser um aliado antirracista.',
            question_type='SA',
            explanation='Exemplos: questionar comentários racistas, apoiar negócios de pessoas negras, educar familiares, participar de movimentos antirracistas, usar privilégios para amplificar vozes marginalizadas, etc.',
            points=15
        )
        QuizQuestion.objects.create(quiz=quiz3, question=q8, order=3)

        self.stdout.write(self.style.SUCCESS(f'✅ Successfully added content to "{course.name}"'))
        self.stdout.write(f'   - {course.modules.count()} modules created')
        self.stdout.write(f'   - {Lesson.objects.filter(module__course=course).count()} lessons created')
        self.stdout.write(f'   - {Quiz.objects.filter(module__course=course).count()} quizzes created')
        self.stdout.write(f'   - {Question.objects.filter(course=course).count()} questions created')
