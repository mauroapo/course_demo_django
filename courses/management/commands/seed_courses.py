from django.core.management.base import BaseCommand
from courses.models import Course


class Command(BaseCommand):
    help = 'Seed database with sample courses'

    def handle(self, *args, **kwargs):
        # Check if courses already exist
        if Course.objects.exists():
            self.stdout.write(self.style.WARNING('Courses already exist. Skipping seed.'))
            return

        courses_data = [
            {
                'name': 'Introdução à Síndrome de Down',
                'description': 'Curso completo sobre os fundamentos da Síndrome de Down, características e desenvolvimento.',
                'price': 99.90,
                'image_url': 'https://images.unsplash.com/photo-1503676260728-1c00da094a0b?w=400&h=300&fit=crop',
            },
            {
                'name': 'Inclusão Escolar',
                'description': 'Estratégias e práticas para promover a inclusão de crianças com Síndrome de Down na escola.',
                'price': 149.90,
                'image_url': 'https://images.unsplash.com/photo-1427504494785-3a9ca7044f45?w=400&h=300&fit=crop',
            },
            {
                'name': 'Desenvolvimento da Linguagem',
                'description': 'Técnicas e atividades para estimular o desenvolvimento da linguagem e comunicação.',
                'price': 129.90,
                'image_url': 'https://images.unsplash.com/photo-1503454537195-1dcabb73ffb9?w=400&h=300&fit=crop',
            },
            {
                'name': 'Alfabetização Inclusiva',
                'description': 'Métodos adaptados de alfabetização para crianças com Síndrome de Down.',
                'price': 179.90,
                'image_url': 'https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?w=400&h=300&fit=crop',
            },
            {
                'name': 'Autonomia e Vida Independente',
                'description': 'Preparando jovens com Síndrome de Down para uma vida mais independente.',
                'price': 159.90,
                'image_url': 'https://images.unsplash.com/photo-1522202176988-66273c2fd55f?w=400&h=300&fit=crop',
            },
            {
                'name': 'Saúde e Bem-Estar',
                'description': 'Cuidados de saúde específicos e promoção do bem-estar para pessoas com Síndrome de Down.',
                'price': 119.90,
                'image_url': 'https://images.unsplash.com/photo-1505751172876-fa1923c5c528?w=400&h=300&fit=crop',
            },
            {
                'name': 'Estimulação Precoce',
                'description': 'Atividades e exercícios para estimulação precoce de bebês e crianças pequenas.',
                'price': 139.90,
                'image_url': 'https://images.unsplash.com/photo-1476703993599-0035a21b17a9?w=400&h=300&fit=crop',
            },
            {
                'name': 'Direitos e Legislação',
                'description': 'Conhecendo os direitos das pessoas com Síndrome de Down e a legislação brasileira.',
                'price': 89.90,
                'image_url': 'https://images.unsplash.com/photo-1450101499163-c8848c66ca85?w=400&h=300&fit=crop',
            },
            {
                'name': 'Preparação para o Mercado de Trabalho',
                'description': 'Desenvolvendo habilidades profissionais e preparando para o mercado de trabalho.',
                'price': 169.90,
                'image_url': 'https://images.unsplash.com/photo-1521737711867-e3b97375f902?w=400&h=300&fit=crop',
            },
            {
                'name': 'Tecnologias Assistivas',
                'description': 'Utilizando tecnologias e recursos para apoiar o aprendizado e desenvolvimento.',
                'price': 149.90,
                'image_url': 'https://images.unsplash.com/photo-1488590528505-98d2b5aba04b?w=400&h=300&fit=crop',
            },
            {
                'name': 'Socialização e Amizades',
                'description': 'Promovendo habilidades sociais e construindo relacionamentos saudáveis.',
                'price': 109.90,
                'image_url': 'https://images.unsplash.com/photo-1529156069898-49953e39b3ac?w=400&h=300&fit=crop',
            },
            {
                'name': 'Música e Arte Terapia',
                'description': 'Usando música e arte como ferramentas terapêuticas e de desenvolvimento.',
                'price': 0.00,  # Free course
                'image_url': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&h=300&fit=crop',
            },
            {
                'name': 'Atividade Física Adaptada',
                'description': 'Exercícios e atividades físicas adaptadas para pessoas com Síndrome de Down.',
                'price': 0.00,  # Free course
                'image_url': 'https://images.unsplash.com/photo-1571019614242-c5c5dee9f50b?w=400&h=300&fit=crop',
            },
            {
                'name': 'Apoio às Famílias',
                'description': 'Orientação e suporte para famílias de pessoas com Síndrome de Down.',
                'price': 99.90,
                'image_url': 'https://images.unsplash.com/photo-1511632765486-a01980e01a18?w=400&h=300&fit=crop',
            },
            {
                'name': 'Combate ao Racismo Inclusivo',
                'description': 'Entendendo e combatendo o racismo inclusivo e a dupla invisibilidade.',
                'price': 0.00,  # Free course
                'image_url': 'https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=400&h=300&fit=crop',
            },
        ]

        created_count = 0
        for course_data in courses_data:
            Course.objects.create(**course_data)
            created_count += 1
            self.stdout.write(self.style.SUCCESS(f'Created course: {course_data["name"]}'))

        self.stdout.write(self.style.SUCCESS(f'\nSuccessfully created {created_count} courses!'))
