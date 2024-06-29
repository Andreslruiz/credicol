import random

from .services import send_cluster_test


def send_cluster_test_message(numbers):

    mensajes_motivacionales = [
        "🌅 *Cada día es una nueva oportunidad para cambiar tu vida.*",
        "🏆 *El éxito es la suma de pequeños esfuerzos repetidos día tras día.*",
        "❤️ *La única forma de hacer un gran trabajo es amar lo que haces.*",
        "⏳ *No cuentes los días, haz que los días cuenten.*",
        "🌳 *El mejor momento para plantar un árbol fue hace 20 años. El segundo mejor momento es ahora.*",
        "💪 *La persistencia puede cambiar el fracaso en un logro extraordinario.*",
        "🌟 *Cree que puedes y ya estás a medio camino.*",
        "😊 *La actitud es una pequeña cosa que hace una gran diferencia.*",
        "🔍 *El pesimista ve dificultad en cada oportunidad. El optimista ve oportunidad en cada dificultad.*",
        "🐢 *No importa lo lento que vayas, siempre y cuando no te detengas.*",
        "⏰ *Tu tiempo es limitado, no lo desperdicies viviendo la vida de alguien más.*",
        "🦁 *El éxito no es definitivo, el fracaso no es fatal: lo que cuenta es el coraje para continuar.*",
        "🔮 *La mejor manera de predecir el futuro es crearlo.*",
        "🕰️ *Nunca es demasiado tarde para ser lo que podrías haber sido.*",
        "📚 *El único lugar donde el éxito viene antes que el trabajo es en el diccionario.*",
        "🌞 *No dejes que ayer ocupe demasiado de hoy.*",
        "🌍 *Sé el cambio que quieres ver en el mundo.*",
        "🎭 *La vida es 10% lo que te sucede y 90% cómo reaccionas a ello.*",
        "💭 *Si puedes soñarlo, puedes hacerlo.*",
        "🚀 *Haz hoy lo que otros no quieren, haz mañana lo que otros no pueden.*",
        "🚪 *Las oportunidades no ocurren, las creas.*",
        "🔥 *El éxito es ir de fracaso en fracaso sin perder el entusiasmo.*",
        "⚡ *La motivación te pone en marcha, el hábito te mantiene en camino.*",
        "🌱 *Tus talentos y habilidades irán mejorando con el tiempo, pero para eso has de empezar.*",
        "🏹 *No te conformes con lo que necesitas, lucha por lo que te mereces.*",
        "✨ *La diferencia entre lo ordinario y lo extraordinario es ese pequeño extra.*",
        "🏔️ *Los desafíos son lo que hacen la vida interesante, superarlos es lo que hace la vida significativa.*",
        "💖 *El único modo de hacer un gran trabajo es amar lo que haces.*",
        "⏳ *No esperes. Nunca habrá un momento perfecto.*",
        "🌠 *Cree en ti mismo y todo será posible.*"
    ]

    for num in numbers:
        message = random.choice(mensajes_motivacionales)
        send_cluster_test(f'+57{num}', message)
