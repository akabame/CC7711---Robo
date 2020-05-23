from controller import Robot, DistanceSensor, Motor

TIME_STEP = 64

#declara a classe do epuck
robot = Robot()
#declara o nome dos sensores
ps = []
psNames = [
    'ps0', 'ps1', 'ps2', 'ps3',
    'ps4', 'ps5', 'ps6', 'ps7'
]
#inicializa os sensores
for i in range(8):
    ps.append(robot.getDistanceSensor(psNames[i]))
    ps[i].enable(TIME_STEP)
#define e iniciliza motores com suas posi��es iniciais
leftMotor = robot.getMotor('left wheel motor')
rightMotor = robot.getMotor('right wheel motor')
leftMotor.setPosition(float('inf'))
rightMotor.setPosition(float('inf'))
leftMotor.setVelocity(0.0)
rightMotor.setVelocity(0.0)

#while vai garantir a implementa��o da velocidade e o desvio de objetos
#por loop
while robot.step(TIME_STEP) != -1:
    
    #guarda o valor de todos os sensores num vetor
    psValues = []
    for i in range(8):
        psValues.append(ps[i].getValue())
    #define variaveis para guardar true ou false em rela��o ao objeto para 
    #um determinado valor de proximidade
    right_obstacle = psValues[0] > 80.0 or psValues[1] > 80.0 or psValues[2] > 80.0
    left_obstacle = psValues[5] > 80.0 or psValues[6] > 80.0 or psValues[7] > 80.0
    
    #declara velocidade m�xima e c�lculo da rota��o das rodas do robo
    MAX_SPEED = 6
    leftSpeed  = 0.5 * MAX_SPEED
    rightSpeed = 0.5 * MAX_SPEED
    
    #####a codifica��o acima est� presente na pr�pria documenta��o do Webots
    
    #####abaixo segue as implementa��es sobre o c�digo b�sico:
    
    #insere os valores dos sensores de esquerda e direita em duas listas
    prox_r = [psValues[0],psValues[1],psValues[2]]
    prox_l = [psValues[5], psValues[6], psValues[7]]
    col_r = max(prox_r)
    col_l = max(prox_l)
    
    #se por motivo do robo se aproxima muito de algum objeto
    #ser� mais seguro ele rotacionar seu eixo central para evitar colis�o
    if col_l >= 200:
        leftSpeed  = MAX_SPEED
        rightSpeed = -MAX_SPEED
    elif col_r >= 200:
        leftSpeed  = -MAX_SPEED
        rightSpeed = MAX_SPEED
    
    #caso n�o esteja muito pr�ximo de objetos, pequenos desvios s�o seguros
    elif left_obstacle or right_obstacle:
        prox_r = max(prox_r)
        prox_l = max(prox_l)
        if prox_r > prox_l:
            leftSpeed  -= 0.5 * MAX_SPEED
            rightSpeed += 0.5 * MAX_SPEED
        elif prox_l > prox_r:
            leftSpeed += 0.5 * MAX_SPEED
            rightSpeed -= 0.5 * MAX_SPEED    
        
    #aplica as velocidades calculadas
    leftMotor.setVelocity(leftSpeed)
    rightMotor.setVelocity(rightSpeed)