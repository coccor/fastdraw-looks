# Writes azure.look, aws.look and gcp.look: FastDraw's built-in look (tools/base-styles.txt) in each cloud's colours and type,
# with group styles for the cloud's boundaries and the cloud's own icons in place of the built-in ones.
# The style names, box sizes and type sizes stay the built-in look's, so a diagram drawn for it switches with one line.
#   python3 tools/gen-cloud-looks.py
import os
import re

import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lookgen import HERE, FONTS, build, colours, fonts, base_styles, write  # noqa: E402

# the type of a group's name: the cloud's own diagrams label groups in plain sans, not spaced capitals
GROUP_TITLE = 'title.font=sans title.size=10 title.weight=600 title.spacing=0 title.caps=0'

def common_edits(radius, accent_tint, cloud_fill, cloud_stroke):
    return {
        # the cloud's icons are colour pictures; a little larger than the built-in outlines, still left of the text
        'node': {'radius': str(radius), 'icon.size': '24'},
        'focal': {'fill': accent_tint, 'stroke': 'accent', 'title.color': 'ink'},
        'terminal-focal': {'fill': accent_tint, 'title.color': 'ink'},
        'cloud': {'fill': cloud_fill, 'stroke': cloud_stroke},
        # on a white page the built-in grey cylinder is too heavy
        'store': {'fill': '#f5f6f7', 'stroke': 'ink/0.22'},
        'zone': {'radius': str(radius), 'fill': 'none', 'stroke': 'ink/0.35', 'title.font': 'sans', 'title.size': '10',
                 'title.weight': '600', 'title.color': 'ink', 'title.spacing': '0', 'title.caps': '0'},
    }

# ---- Azure ------------------------------------------------------------------------------------------------
def azure(base):
    c = {'paper': '#ffffff', 'card': '#ffffff', 'ink': '#323130', 'muted': '#605e5c', 'soft': '#a19f9d',
         'accent': '#0078d4', 'link': '#0063b1', 'teal': '#008575', 'amber': '#c19c00', 'rose': '#d13438', 'violet': '#8661c5'}
    edits = common_edits(2, '#eff6fc', '#f3f9fd', 'accent/0.45')
    groups = [
        f'style subscription extends zone stroke=#ffb900 sw=1.2 {GROUP_TITLE} title.color=ink use="an Azure subscription; always give WxH"',
        f'style resource-group extends zone stroke=ink/0.45 dash=5,4 {GROUP_TITLE} title.color=ink use="a resource group; always give WxH"',
        f'style vnet extends zone fill=#0078d4/0.04 stroke=#0078d4 sw=1.2 {GROUP_TITLE} title.color=#0063b1 use="a virtual network; always give WxH"',
        f'style subnet extends zone fill=#0078d4/0.05 stroke=#0078d4/0.6 dash=4,3 {GROUP_TITLE} title.color=#0063b1 use="a subnet inside a virtual network; always give WxH"',
    ]
    head = ['Azure: FastDraw\'s built-in look in the colours of Azure\'s architecture diagrams. A white page, square cards,',
            'Azure blue for the subject and the main path, Open Sans, and Azure\'s own service icons (icon=app-service).',
            'Groups for a subscription, a resource group, a virtual network and a subnet. Same style names as the built-in look.']
    settings = ['canvas paper=paper dots=none', '', *colours(c), '', *fonts('Open Sans'), '',
                '// Azure\'s service icons, from Ben Coleman\'s icon collection (MIT) at a fixed commit, by their short names',
                'icondir "https://cdn.jsdelivr.net/gh/benc-uk/icon-collection@e33ee714d05a24a81cf6ccd967ef34b22cb77e65/azure-docs/{name}.svg"',
                'icons builtin=hidden']
    guidance = ['Icons are Azure\'s own, by short name: icon=app-service, functions, sql-database, cosmos-db, storage-accounts, key-vault, api-management, front-door, application-gateways, kubernetes-services, container-instances, service-bus, event-hubs, monitor, application-insights, virtual-machine. fastdraw icons <look> lists them all.',
                'Put resources in a vnet and subnets in it when the network matters; use resource-group or subscription for ownership.']
    return build(base, edits, groups, head, settings, [], guidance)

# ---- AWS --------------------------------------------------------------------------------------------------
# Short names for the services diagrams name most; every other icon is named from its file (AWSAppRunner -> app-runner).
AWS_SHORT = {
    'AmazonAPIGateway': 'api-gateway', 'AmazonAurora': 'aurora', 'AmazonAthena': 'athena', 'AmazonBedrock': 'bedrock',
    'AmazonCloudFront': 'cloudfront', 'AmazonCloudWatch': 'cloudwatch', 'AmazonCognito': 'cognito', 'AmazonDocumentDB': 'documentdb',
    'AmazonDynamoDB': 'dynamodb', 'AmazonEC2': 'ec2', 'AmazonEC2AutoScaling': 'ec2-auto-scaling', 'AmazonElasticBlockStore': 'ebs',
    'AmazonElasticContainerRegistry': 'ecr', 'AmazonElasticContainerService': 'ecs', 'AmazonElasticKubernetesService': 'eks',
    'AmazonEFS': 'efs', 'AmazonElastiCache': 'elasticache', 'AmazonEMR': 'emr', 'AmazonEventBridge': 'eventbridge',
    'AmazonKinesis': 'kinesis', 'AmazonKinesisDataStreams': 'kinesis-data-streams', 'AmazonDataFirehose': 'firehose',
    'AmazonManagedStreamingforApacheKafka': 'msk', 'AmazonMQ': 'mq', 'AmazonNeptune': 'neptune', 'AmazonOpenSearchService': 'opensearch',
    'AmazonRDS': 'rds', 'AmazonRedshift': 'redshift', 'AmazonRoute53': 'route53', 'AmazonSageMaker': 'sagemaker',
    'AmazonSimpleStorageService': 's3', 'AmazonSimpleStorageServiceGlacier': 's3-glacier', 'AmazonSimpleEmailService': 'ses',
    'AmazonSimpleNotificationService': 'sns', 'AmazonSimpleQueueService': 'sqs', 'AmazonVirtualPrivateCloud': 'vpc',
    'AmazonMemoryDB': 'memorydb', 'AmazonTimestream': 'timestream', 'AmazonQ': 'amazon-q', 'AmazonLightsail': 'lightsail',
    'AWSLambda': 'lambda', 'AWSFargate': 'fargate', 'AWSStepFunctions': 'step-functions', 'AWSIdentityandAccessManagement': 'iam',
    'AWSIAMIdentityCenter': 'iam-identity-center', 'AWSKeyManagementService': 'kms', 'AWSSecretsManager': 'secrets-manager',
    'AWSWAF': 'waf', 'AWSShield': 'shield', 'AWSCloudFormation': 'cloudformation', 'AWSCloudTrail': 'cloudtrail',
    'AWSCodePipeline': 'codepipeline', 'AWSCodeBuild': 'codebuild', 'AWSCodeDeploy': 'codedeploy', 'AWSCodeCommit': 'codecommit',
    'AWSAppRunner': 'app-runner', 'AWSAmplify': 'amplify', 'AWSAppSync': 'appsync', 'AWSBatch': 'batch', 'AWSBackup': 'backup',
    'AWSGlue': 'glue', 'AWSXRay': 'x-ray', 'ElasticLoadBalancing': 'elb', 'AWSTransitGateway': 'transit-gateway',
    'AWSDirectConnect': 'direct-connect', 'AWSCertificateManager': 'acm', 'AWSSystemsManager': 'systems-manager',
    'AWSOrganizations': 'organizations', 'AWSPrivateLink': 'privatelink', 'AWSGlobalAccelerator': 'global-accelerator',
    'AWSIoTCore': 'iot-core', 'AWSElasticBeanstalk': 'elastic-beanstalk', 'AWSDatabaseMigrationService': 'dms',
    'AWSDataSync': 'datasync', 'AWSTransferFamily': 'transfer-family', 'AWSSitetoSiteVPN': 'site-to-site-vpn',
    'AWSClientVPN': 'client-vpn', 'AWSNetworkFirewall': 'network-firewall', 'AWSConfig': 'config', 'AWSCloudMap': 'cloud-map',
    'AWSAppMesh': 'app-mesh', 'AWSOutpostsfamily': 'outposts', 'AWSSecurityHub': 'security-hub', 'AmazonGuardDuty': 'guardduty',
    'AmazonInspector': 'inspector', 'AmazonMacie': 'macie', 'AmazonManagedGrafana': 'grafana',
    'AmazonManagedServiceforPrometheus': 'prometheus', 'AmazonManagedWorkflowsforApacheAirflow': 'mwaa',
}

def kebab(file):
    s = re.sub(r'^(Amazon|AWS)(?=[A-Z])', '', file)
    s = s.replace('IoT', 'Iot').replace('FSx', 'Fsx').replace('rePost', 'Repost')
    words = re.findall(r'[A-Z]+\d*(?=[A-Z][a-z]|$)|[A-Z]?[a-z]+\d*|[A-Z]+\d+|\d+', s)
    return '-'.join(w.lower() for w in words)

AWS_GROUPS = {'group-aws-cloud': 'AWSCloudlogo', 'group-cloud': 'AWSCloud', 'group-account': 'AWSAccount', 'group-region': 'Region',
              'group-vpc': 'VirtualprivatecloudVPC', 'group-public-subnet': 'Publicsubnet', 'group-private-subnet': 'Privatesubnet',
              'group-auto-scaling': 'AutoScalinggroup', 'group-data-center': 'Corporatedatacenter', 'group-ec2-contents': 'EC2instancecontents',
              'group-spot-fleet': 'SpotFleet', 'group-server-contents': 'Servercontents'}
AWS_GENERIC = {'users': 'Users', 'user': 'User', 'client': 'Client', 'mobile-client': 'Mobileclient', 'internet': 'Internet',
               'generic-application': 'GenericApplication', 'office-building': 'Officebuilding', 'authenticated-user': 'AuthenticatedUser'}

def aws_icons():
    files = [l.strip() for l in open(os.path.join(HERE, 'aws-icons.txt')) if l.strip()]
    names, out = {}, []
    for f in files:
        n = AWS_SHORT.get(f) or kebab(f)
        if not re.fullmatch(r'[a-z0-9]+(-[a-z0-9]+)*', n) or n in names:
            raise SystemExit(f'{f}: name {n!r} is not usable or is taken by {names.get(n)}')
        names[n] = f
    for n in sorted(names):
        out.append(f'icon {n} "https://cdn.jsdelivr.net/npm/aws-icons@3.3.0/icons/architecture-service/{names[n]}.svg"')
    for n, f in AWS_GENERIC.items():
        if n in names:
            raise SystemExit(f'{n} is both a service and a generic icon')
        out.append(f'icon {n} "https://cdn.jsdelivr.net/npm/aws-icons@3.3.0/icons/resource/{f}.svg"')
    for n, f in AWS_GROUPS.items():
        out.append(f'icon {n} "https://cdn.jsdelivr.net/npm/aws-icons@3.3.0/icons/architecture-group/{f}.svg"')
    return out

def aws(base):
    """AWS as its documentation draws it (the AWS Solutions diagrams): no boxes, each service a large icon with its name
    under it; groups are frames with the group's icon as a tab in the top-left corner; dark lines with open heads."""
    c = {'paper': '#ffffff', 'card': '#ffffff', 'ink': '#232f3e', 'muted': '#232f3e', 'soft': '#7d8998',
         'accent': '#ed7100', 'link': '#232f3e', 'teal': '#01a88d', 'amber': '#ed7100', 'rose': '#e7157b', 'violet': '#8c4fff'}
    # a service is its icon with the name under it and no box; the box is still there to place it and end lines on
    bare = {'fill': 'none', 'stroke': 'none', 'icon.pos': 'top', 'icon.size': '48', 'title.size': '13', 'title.weight': '400',
            'title.color': 'ink', 'sub.font': 'sans', 'sub.size': '11', 'sub.italic': '1', 'sub.color': 'ink',
            'tag.color': 'ink', 'tag.border': 'ink/0.5'}
    boxed = {'fill': '#ffffff', 'stroke': 'ink', 'sw': '1.5', 'icon.pos': 'left', 'icon.size': '20', 'title.size': '12', 'title.weight': '400',
             'sub.size': '10', 'sub.italic': '1'}
    edits = {
        'node': {'radius': '0', 'size': '144x104', **bare},
        # the subject: the one service with a tint behind it
        'focal': {**bare, 'fill': '#fdf0e3', 'radius': '4', 'title.weight': '700'},
        'store': {**bare, 'shape': 'rect'},
        'cloud': bare,
        # people and devices: AWS's generic outline icons
        'external': {**bare, 'icon': 'users'},
        'optional': {**bare, 'stroke': 'soft', 'dash': '4,3'},
        'sticky': {'fill': '#fff7d6', 'stroke': 'ink/0.4', 'icon.pos': 'left', 'icon.size': '20', 'title.size': '12', 'sub.italic': '0'},
        'sticky-orange': {'fill': '#ffe8d9'},
        'sticky-violet': {'fill': '#efe7ff'},
        'step': boxed, 'terminal': boxed,
        'terminal-focal': {**boxed, 'fill': '#fdf0e3', 'stroke': 'accent', 'sw': '2', 'title.color': 'ink'},
        'decision': {'fill': '#ffffff', 'stroke': 'ink', 'sw': '1.5'},
        # a generic group: a dashed grey frame; given an icon, it shows it as a tab in the corner
        'zone': {'radius': '0', 'fill': 'none', 'stroke': 'soft', 'sw': '1.5', 'dash': '4,3', 'icon.pos': 'corner', 'icon.size': '32',
                 'title.font': 'sans', 'title.size': '13', 'title.weight': '400', 'title.color': 'ink', 'title.spacing': '0', 'title.caps': '0',
                 'title.dy': '3.5', 'title.fill': 'none'},
        'bar': {'fill': 'accent/0.15', 'stroke': 'accent'},
        'table': {'radius': '0', 'stroke': 'ink', 'sw': '1.5', 'head.fill': '#f2f3f3', 'rule': 'ink/0.15'},
        # dark lines with open heads, square turns
        'arrow': {'stroke': 'ink', 'sw': '2', 'radius': '0', 'head': 'open', 'label.color': 'ink', 'label.size': '11', 'label.italic': '1'},
        'primary': {'stroke': 'accent', 'sw': '2.5', 'label.color': 'ink', 'label.weight': '600'},
        'link': {'stroke': 'ink', 'label.color': 'ink'},
        'return': {'dash': '6,4'},
        'relation': {'stroke': 'ink'},
        'kicker': {'color': '#ed7100'},
    }
    def group(name, icon, colour, use, extra=''):
        return (f'style {name} extends zone stroke={colour} sw=2 dash=none icon={icon} title.color=ink {extra}'
                f' use="{use}; always give WxH"').replace('  ', ' ')
    groups = [
        group('aws-cloud', 'group-aws-cloud', '#232f3e', 'the AWS Cloud: a dark frame with the AWS logo in the corner'),
        group('cloud-group', 'group-cloud', '#232f3e', 'a part of AWS, such as an account by its owner: a dark frame with a cloud in the corner'),
        group('account', 'group-account', '#e7157b', 'an AWS account: a pink frame with the account icon'),
        group('region', 'group-region', '#01a88d', 'an AWS Region: a dashed teal frame with a flag', 'dash=5,4 sw=1.5'),
        group('vpc', 'group-vpc', '#8c4fff', 'a VPC: a purple frame'),
        group('public-subnet', 'group-public-subnet', '#7aa116', 'a public subnet: a green panel', 'fill=#f2f6e8 stroke=none'),
        group('private-subnet', 'group-private-subnet', '#01a88d', 'a private subnet: a teal panel', 'fill=#e6f6f7 stroke=none'),
        group('auto-scaling', 'group-auto-scaling', '#ed7100', 'an Auto Scaling group: a dashed orange frame', 'dash=5,4'),
        group('data-center', 'group-data-center', '#7d8998', 'a corporate data center: a grey frame'),
        'style az extends zone stroke=#01a88d sw=1.5 dash=5,4 use="an Availability Zone: a dashed teal frame; always give WxH"',
        'style security-group extends zone stroke=#dd344c sw=1.5 dash=3,3 use="a security group: a dashed red frame; always give WxH"',
        # the black circles AWS diagrams number their flow with
        'style callout shape=ellipse size=32x32 fill=ink stroke=none title.color=#ffffff title.size=14 title.weight=700'
        ' use="a numbered step of the flow, a black circle: callout \\"1\\" at x,y (32x32)"',
    ]
    head = ['AWS: drawn the way the AWS Solutions documentation draws architecture. No boxes: each service is its 48px AWS icon with',
            'the name under it and an italic second line; people and devices are AWS\'s generic icons. Groups are frames with the',
            'group\'s icon as a tab in the top-left corner (the AWS Cloud logo, a cloud, an account, a Region flag, a VPC, a subnet),',
            'lines are dark with open heads, and callout numbers the flow in black circles. Arimo (Arial\'s widths). Same style',
            'names as the built-in look; a service\'s box is 144x104, to hold the icon above the name.']
    settings = ['canvas paper=paper dots=none', '', *colours(c), '', *fonts('Arimo'), '',
                '// the AWS architecture icons (the aws-icons package, at a fixed version), each named below',
                'icons builtin=hidden']
    guidance = ['Each service is its icon with the name under it: give every box an icon (icon=lambda, s3, dynamodb, rds, aurora, ec2, ecs, eks, fargate, api-gateway, cloudfront, route53, elb, sqs, sns, eventbridge, step-functions, kinesis, cognito, iam, kms, secrets-manager, cloudwatch); people and devices are icon=users, user, client, mobile-client, internet. Name a service as AWS does (Amazon S3, AWS Lambda) and put its role in sub=. fastdraw icons <look> lists every icon.',
                'Boxes are 144x104: leave about 140px between rows. Nest groups the way AWS does: aws-cloud, then account or cloud-group, region, vpc, az, public-subnet or private-subnet; zone is a dashed generic group, and given icon=<a service> it shows that icon as its tab (a Step Functions workflow: icon=step-functions).',
                'Number the steps of the flow with callout "1", callout "2" beside the lines they describe.']
    return build(base, edits, groups, head, settings, aws_icons(), guidance)


# ---- Google Cloud -----------------------------------------------------------------------------------------
GCP_RGB = ['apigee', 'cloudrun', 'computeengine', 'networking', 'secops']

def gcp(base):
    """Google Cloud as its architecture docs draw it (the Enterprise Application Blueprint): white cards with heavy dark
    outlines and the product icon on the left, nested coloured panels with the name centred at the top, dark lines with
    open heads, dashed for the control plane."""
    c = {'paper': '#ffffff', 'card': '#ffffff', 'ink': '#202124', 'muted': '#3c4043', 'soft': '#80868b',
         'accent': '#1a73e8', 'link': '#202124', 'teal': '#137333', 'amber': '#b06000', 'rose': '#c5221f', 'violet': '#8430ce'}
    card = {'radius': '4', 'fill': '#ffffff', 'stroke': '#1f2124', 'sw': '2', 'title.size': '12', 'title.weight': '600', 'title.color': 'ink',
            'sub.font': 'sans', 'sub.color': 'muted', 'icon.size': '28', 'tag.color': 'ink', 'tag.border': 'ink/0.5'}
    panel = {'radius': '4', 'stroke': '#1f2124', 'sw': '1', 'dash': 'none', 'title.font': 'sans', 'title.size': '12', 'title.weight': '400',
             'title.color': 'ink', 'title.spacing': '0', 'title.caps': '0', 'title.align': 'center', 'title.dy': '6', 'title.fill': 'none'}
    edits = {
        'node': card,
        'focal': {'fill': '#e8f0fe', 'stroke': 'accent', 'sw': '2.5', 'title.color': 'ink', 'tag.color': 'ink', 'tag.border': 'ink'},
        # data, and replicas, as a card with a grey card behind it
        'store': {'shape': 'rect', 'fill': '#ffffff', 'stroke': '#1f2124', 'sw': '2', 'depth': '5', 'depth.fill': '#bec1c6', 'depth.stroke': '#1f2124'},
        'cloud': {'fill': '#e8f0fe', 'stroke': '#1f2124', 'sw': '2'},
        'external': {'fill': '#ffffff', 'stroke': '#1f2124', 'sw': '2', 'dash': 'none', 'icon': 'user', 'icon.color': 'ink', 'icon.fill': 'none'},
        'optional': {'fill': '#ffffff', 'stroke': '#1f2124', 'sw': '1.5', 'dash': '6,5'},
        'sticky': {'fill': '#ffeebd', 'stroke': '#1f2124', 'sw': '1'},
        'sticky-orange': {'fill': '#fad2cf'},
        'sticky-violet': {'fill': '#e9d2fd'},
        'terminal': {'fill': '#ffffff', 'stroke': '#1f2124', 'sw': '2'},
        'terminal-focal': {'fill': '#e8f0fe', 'stroke': 'accent', 'sw': '2.5', 'title.color': 'ink'},
        'decision': {'fill': '#ffffff', 'stroke': '#1f2124', 'sw': '2'},
        # a plain group: a grey panel, its name centred at the top
        'zone': {**panel, 'fill': '#f1f3f4'},
        'bar': {'fill': '#aecbfa', 'stroke': '#1f2124'},
        'table': {'radius': '4', 'stroke': '#1f2124', 'sw': '2', 'head.fill': '#f1f3f4', 'rule': 'ink/0.2'},
        'arrow': {'stroke': 'ink', 'sw': '1.6', 'radius': '0', 'head': 'open', 'head.size': '0.9', 'label.color': 'ink', 'label.size': '9.5', 'label.weight': '600'},
        'primary': {'stroke': 'accent', 'sw': '2.4', 'label.color': 'ink'},
        'link': {'stroke': 'ink', 'label.color': 'ink'},
        # the control plane: dashed
        'return': {'dash': '6,5'},
        'relation': {'stroke': 'ink'},
        'legend': {'rule': 'ink/0.3'},
        'kicker': {'color': '#1a73e8'},
    }
    groups = [
        'style project extends zone fill=#aecbfa use="a Google Cloud project: a light blue panel; always give WxH"',
        'style region extends zone fill=#f1f3f4 use="a region: a grey panel; always give WxH"',
        'style gke-cluster extends zone fill=#669df6 use="a GKE cluster: a blue panel; always give WxH"',
        'style namespace extends zone fill=#ffeebd use="a Kubernetes namespace or a tenant: a yellow panel; always give WxH"',
        'style service-group extends zone fill=#ffffff use="a service and what runs in it: a white panel; always give WxH"',
        'style google-cloud extends zone fill=#4285f4 title.align=left title.size=14 title.weight=500 title.color=#ffffff use="the Google Cloud boundary: a blue panel with the name in white; always give WxH"',
        'style vpc extends zone fill=none dash=6,5 use="a VPC network: a dashed frame; always give WxH"',
        'style on-premises extends zone fill=#ffffff dash=6,5 use="systems outside Google Cloud: a dashed frame; always give WxH"',
        'style subsystem-blue extends zone fill=#e8f0fe dash=4,3 use="a subsystem: a pale blue panel with a dashed outline; always give WxH"',
        'style subsystem-green extends zone fill=#e3f5e9 dash=4,3 use="a subsystem: a pale green panel with a dashed outline; always give WxH"',
    ]
    head = ['Google Cloud: drawn the way Google Cloud\'s architecture docs draw diagrams (the Enterprise Application Blueprint).',
            'White cards with heavy dark outlines and the product icon on the left, data as a card with a grey card behind it,',
            'nested panels with the name centred at the top (a project light blue, a region grey, a GKE cluster blue, a namespace',
            'yellow), dark lines with open heads, dashed for the control plane, Google Sans, and Google Cloud\'s product icons',
            '(icon=bigquery, icon=gke). Same style names as the built-in look.']
    base_url = 'https://cdn.jsdelivr.net/npm/gcp-icons@1.0.6/dist/icons/'
    settings = ['canvas paper=paper dots=none', '', *colours(c), '', *fonts('Google Sans 18pt'), '',
                '// Google Cloud\'s product and category icons (the gcp-icons package, at a fixed version), by their names',
                f'icondir "{base_url}{{name}}-512-color.svg"', 'icons builtin=hidden']
    icons = [f'icon {n} "{base_url}{n}-512-color-rgb.svg"' for n in GCP_RGB]
    guidance = ['Icons are Google Cloud\'s, by name: icon=cloudrun, computeengine, gke, cloud-storage, cloudsql, cloudspanner, alloydb, bigquery, vertexai, apigee, looker, networking. The set has 45 product and category icons; fastdraw icons <look> lists them.',
                'Nest panels as Google Cloud does: project, then region, then gke-cluster, then namespace, then service-group; leave 32px at the top of each panel for its name. Draw the control plane with style=return (dashed) and say so in a legend.']
    return build(base, edits, groups, head, settings, icons, guidance)


# ---- Kubernetes -------------------------------------------------------------------------------------------
# The project's own icons (kubernetes/community, Apache 2.0): the labeled heptagons the documentation draws, with
# the short name inside. They are kept in this repository with that name turned into outlines (tools/k8s-icons.sh),
# because a PNG renderer (resvg) draws no text inside an SVG it shows as an image.
K8S = 'https://raw.githubusercontent.com/coccor/fastdraw-looks/main/icons/kubernetes/'
K8S_RESOURCES = ['c-role', 'cm', 'crb', 'crd', 'cronjob', 'deploy', 'ds', 'ep', 'group', 'hpa', 'ing', 'job', 'limits', 'netpol', 'ns', 'pod',
                 'psp', 'pv', 'pvc', 'quota', 'rb', 'role', 'rs', 'sa', 'sc', 'secret', 'sts', 'svc', 'user', 'vol']
K8S_INFRA = ['control-plane', 'etcd', 'node']
K8S_CONTROL = ['api', 'c-c-m', 'c-m', 'k-proxy', 'kubelet', 'sched']
# the full names of the resources and components whose icon files are named by their short form
K8S_LONG = {'cluster-role': 'c-role', 'configmap': 'cm', 'cluster-role-binding': 'crb', 'deployment': 'deploy', 'daemonset': 'ds',
            'endpoints': 'ep', 'ingress': 'ing', 'limit-range': 'limits', 'network-policy': 'netpol', 'namespace': 'ns',
            'pod-security-policy': 'psp', 'persistent-volume': 'pv', 'persistent-volume-claim': 'pvc', 'resource-quota': 'quota',
            'role-binding': 'rb', 'replicaset': 'rs', 'service-account': 'sa', 'storage-class': 'sc', 'statefulset': 'sts',
            'service': 'svc', 'volume': 'vol', 'autoscaler': 'hpa'}
K8S_CONTROL_LONG = {'api-server': 'api', 'cloud-controller-manager': 'c-c-m', 'controller-manager': 'c-m', 'kube-proxy': 'k-proxy',
                    'scheduler': 'sched'}

def kubernetes(base):
    """Kubernetes as kubernetes.io draws it: each resource its blue heptagon with the name under it, a cluster as a
    light blue panel holding the control plane and the nodes, a Deployment as a black rounded frame with its icon on the
    corner, labels on green plates; flow steps as solid blue boxes, clients as grey pills, line labels on grey plates."""
    c = {'paper': '#ffffff', 'card': '#ffffff', 'ink': '#000000', 'muted': '#555555', 'soft': '#999999',
         'accent': '#326ce5', 'link': '#333333', 'teal': '#0d9488', 'amber': '#b45309', 'rose': '#b85450', 'violet': '#6d28d9'}
    # a resource is its heptagon with the name under it, and no box
    bare = {'radius': '0', 'fill': 'none', 'stroke': 'none', 'icon.pos': 'top', 'icon.size': '56', 'title.size': '13', 'title.weight': '600',
            'title.color': 'ink', 'sub.font': 'sans', 'sub.size': '11', 'sub.color': 'muted', 'tag.color': 'ink', 'tag.border': 'ink/0.4'}
    # a step of a flow: the solid blue box of the Ingress and Gateway diagrams
    blue = {'radius': '0', 'fill': '#326ce5', 'stroke': 'none', 'title.color': '#ffffff', 'title.weight': '700', 'sub.font': 'sans',
            'sub.color': '#ffffff/0.85', 'tag.color': '#ffffff', 'tag.border': '#ffffff/0.6', 'icon.color': '#ffffff', 'icon.fill': 'none'}
    grey = {'fill': '#dddddd', 'stroke': 'none', 'title.color': '#000000', 'title.weight': '400', 'sub.font': 'sans', 'sub.color': 'muted',
            'tag.color': '#000000', 'tag.border': '#000000/0.4', 'icon.color': '#000000', 'icon.fill': 'none'}
    edits = {
        'node': {'size': '144x112', **bare},
        # the subject: the heptagon on a pale blue card, its name in Kubernetes blue
        'focal': {**bare, 'radius': '10', 'fill': '#e6eefc', 'title.color': '#326ce5', 'title.weight': '700'},
        'store': {**bare, 'shape': 'rect'},
        # what lies outside the cluster (a cloud provider's API): a blue pill with white words
        'cloud': {**blue, 'radius': '32'},
        # people and clients: the grey pill of the flow diagrams
        'external': {**grey, 'size': '144x56', 'radius': '28', 'dash': 'none', 'icon.pos': 'left', 'icon.size': '20'},
        'optional': {**bare, 'title.color': 'muted', 'title.weight': '400'},
        # labels and selectors: the green and red plates of the Labels and Selectors diagram
        'sticky': {'radius': '0', 'fill': '#d5e8d4', 'stroke': 'none', 'title.color': '#666666', 'title.weight': '400', 'title.size': '13',
                   'sub.color': '#666666', 'tag.color': '#666666'},
        'sticky-orange': {'fill': '#f8cecc', 'stroke': '#b85450', 'sw': '1.2'},
        'sticky-violet': {'fill': '#ffffff', 'stroke': '#d5e8d4', 'sw': '1.5'},
        'step': blue, 'terminal': {**grey, 'radius': '32'},
        'terminal-focal': {**blue, 'inner': '#ffffff', 'inner.gap': '3', 'inner.sw': '1.2'},
        'decision': {'fill': '#dddddd', 'stroke': 'none', 'title.color': '#000000'},
        # a workload and what it owns: a black rounded frame, its icon on the corner, as a Deployment is drawn
        'zone': {'radius': '18', 'fill': 'none', 'stroke': '#000000', 'sw': '3', 'dash': 'none', 'icon.pos': 'corner', 'icon.size': '48',
                 'title.font': 'sans', 'title.size': '13', 'title.weight': '600', 'title.color': 'ink', 'title.spacing': '0', 'title.caps': '0',
                 'title.align': 'left', 'title.dy': '6', 'title.fill': 'none'},
        'bar': {'fill': '#326ce5/0.2', 'stroke': '#326ce5'},
        'table': {'radius': '0', 'stroke': '#bbbbbb', 'head.fill': '#326ce5/0.12', 'rule': 'ink/0.12'},
        'arrow': {'stroke': '#000000', 'sw': '1.8', 'radius': '0', 'label.color': '#000000', 'label.fill': '#e8e8e8', 'label.border': 'none',
                  'label.size': '11'},
        'primary': {'stroke': '#326ce5', 'sw': '2.4', 'label.color': '#000000'},
        # a request from outside: dotted, as in the Ingress and Gateway diagrams
        'link': {'stroke': '#333333', 'dash': '2,3', 'label.color': '#000000'},
        'return': {'dash': '5,4'},
        # a selector picking its pods: the grey lines of the Labels and Selectors diagram
        'relation': {'stroke': '#666666', 'sw': '1.6'},
        'kicker': {'color': '#326ce5'},
    }
    T_ = 'icon=none title.font=sans title.weight=700 title.spacing=0 title.caps=0 title.align=left'
    groups = [
        f'style cluster extends zone radius=12 fill=#dbe8fb stroke=none sw=0 {T_} title.size=17 title.color=#333333 title.dy=8'
        ' use="a Kubernetes cluster: a light blue panel with its name in large bold type; always give WxH"',
        f'style control-plane extends zone radius=12 fill=#f2f6fd stroke=none sw=0 {T_} title.size=13 title.color=#333333'
        ' use="the control plane: a pale panel inside a cluster; always give WxH"',
        f'style k8s-node extends zone radius=10 fill=#9db4de stroke=none sw=0 {T_} title.size=13 title.color=#222222'
        ' use="a worker node (a machine in the cluster): a darker blue panel; always give WxH"',
        f'style namespace extends zone radius=0 fill=#ffffff stroke=#bbbbbb sw=2 {T_} title.size=12 title.weight=600 title.color=#326ce5'
        ' use="a namespace: a white frame with a grey border, as in the Ingress diagrams; always give WxH"',
        'style pod-group extends zone radius=14 sw=2.5 icon.size=40'
        ' use="what a ReplicaSet or Job owns: a thinner black frame, nested in its Deployment\'s zone (give it icon=rs); always give WxH"',
        'style k8s-label extends sticky size=104x32 use="a label on a resource, a green plate: k8s-label \\"app: A\\" beside the pod"',
        'style selector extends sticky-orange size=104x32 use="a Service\'s selector, a red plate: selector \\"app=A\\" beside the Service"',
    ]
    head = ['Kubernetes: drawn the way kubernetes.io draws its diagrams. Each resource is the project\'s blue heptagon with its short',
            'name inside (pod, svc, deploy, api) and its name under it; a cluster is a light blue panel holding a pale control-plane',
            'panel and darker node panels (Components of Kubernetes); a Deployment is a black rounded frame with its icon on the',
            'corner, labels and selectors are green and red plates (Labels and Selectors). Flow steps are solid blue boxes, clients',
            'grey pills, requests dotted, line labels on grey plates (Ingress, Gateway). Open Sans. Same style names as the built-in',
            'look; a resource\'s box is 144x112, to hold the icon above the name.']
    settings = ['canvas paper=paper dots=none', '', *colours(c), '', *fonts('Open Sans'), '',
                '// the labeled icons of kubernetes/community (Apache 2.0), their names in outline, by kubectl\'s short names',
                f'icondir "{K8S}{{name}}.svg"',
                f'    names="{" ".join(K8S_RESOURCES + K8S_INFRA + K8S_CONTROL)}"',
                'icons builtin=hidden']
    icons = [f'icon {n} "{K8S}{short}.svg"' for n, short in sorted({**K8S_CONTROL_LONG, **K8S_LONG}.items())]
    guidance = ['Give every resource its icon, by kubectl\'s short name or the full one: icon=pod, svc (service), deploy (deployment), rs, sts, ds, ing, job, cronjob, cm, secret, pvc, pv, hpa, ns, sa; the control plane\'s parts are icon=api, sched, c-m, c-c-m, kubelet, k-proxy, etcd, and a machine is icon=node. Resource boxes are 144x112: leave about 144px between rows.',
                'Draw a cluster as cluster, with a control-plane panel and k8s-node panels inside. A Deployment and its pods go in a zone with icon=deploy, its ReplicaSet in a pod-group with icon=rs inside it. Put k8s-label plates beside pods and a selector plate beside their Service, joined with style=relation. For a request flow (Ingress, Gateway) use step boxes, an external client and style=link for the request.']
    return build(base, edits, groups, head, settings, icons, guidance)

if __name__ == '__main__':
    base = base_styles()
    for name, make in [('azure', azure), ('aws', aws), ('gcp', gcp), ('kubernetes', kubernetes)]:
        write(name, make(base))
    print('wrote azure.look, aws.look, gcp.look, kubernetes.look')
